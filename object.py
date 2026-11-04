from __future__ import annotations
import json
from pathlib import Path
import zlib


class GitObject:
    def __init__(self, obj_type: str, content: bytes):
        self.obj_type = obj_type
        self.content = content

    def hash(self) -> str:
        """计算对象的哈希值（SHA-1）"""
        import hashlib
        # 转换为字节的格式：<type> <size>\0<content>
        header = f"{self.obj_type} {len(self.content)}\0".encode()
        store = header + self.content
        return hashlib.sha1(store).hexdigest()

    def serialize(self) -> bytes:
        """序列化对象为字节流"""
        header = f"{self.obj_type} {len(self.content)}\0".encode()
        return zlib.compress(header + self.content)

    @classmethod   
    def deserialize(cls, data: bytes) -> GitObject: 
        """反序列化字节流为对象"""
        # 解压缩得到原始字节数据
        decompressed = zlib.decompress(data)
        # 查找第一个空字节的位置，以分离头部和内容
        null_index = decompressed.index(b'\0')
        # 分离头部和内容
        header = decompressed[:null_index]
        content = decompressed[null_index + 1:]

        # 解析头部信息，获取对象类型和内容大小
        obj_type, size_str = header.decode().split(' ')
        size = int(size_str)

        # 验证内容大小是否与头部信息匹配
        if size != len(content):
            raise ValueError("Content size does not match header size.")

        return GitObject(obj_type, content)

class Blob(GitObject):
    def __init__(self, content: bytes):
        super().__init__('blob', content)

    def get_content(self) -> bytes:
        """获取 BLOB 对象的内容"""
        return self.content
    

class GitRepository:
    def __init__(self, path):
        # 初始化 Git 仓库对象
        self.path = Path(path).resolve()
        self.pygit_dir = self.path / '.pygit'

        self.objects_dir = self.pygit_dir / 'objects'

        self.refs_dir = self.pygit_dir / 'refs'
        self.heads_dir = self.refs_dir / 'heads'

        self.head_file = self.pygit_dir / 'HEAD'

        self.index_file = self.pygit_dir / 'index'

    def init(self) -> bool:
        if self.pygit_dir.exists():
            return False
        
        # 创建 .pygit 目录以及其子目录
        self.pygit_dir.mkdir()
        self.objects_dir.mkdir(exist_ok=True)
        self.refs_dir.mkdir(exist_ok=True)
        self.heads_dir.mkdir(exist_ok=True)

        # 创建 HEAD 文件并指向默认分支
        self.head_file.write_text('ref: refs/heads/kosmigen\n')
        # 创建 index 文件并初始化为空字典
        self._save_index({})

        print(f"Initialized empty PyGit repository in {self.pygit_dir}")
        
        return True

    def add_file(self, file_path: Path):
        full_path = file_path.resolve()
        if not full_path.is_file():
            raise FileNotFoundError(f"File '{full_path}' does not exist.")

        # 以字节形式读取文件中数据
        file_content = full_path.read_bytes()
        # 根据 file_content 创建 BLOB 对象并将其存储在 .pygit/objects 目录中
        blob = Blob(file_content)
        blob_hash = self._store_object(blob)
        # 更新 index 文件，将文件路径和对应的 BLOB 哈希值添加到索引中
        index = self._json_load()
        index[str(file_path.relative_to(self.path))] = blob_hash
        # 保存更新后的索引数据到 index 文件中
        self._save_index(index)

        print(f"Added file '{file_path.relative_to(self.path)}' to staging area with hash {blob_hash}.")

    def add_directory(self, dir_path: Path):
            """将目录中的所有文件递归地添加到暂存区"""
            full_path = dir_path.resolve()

            # rglob('*') 本身已经是递归遍历，直接处理其中的文件即可
            # 返回一个生成器，遍历目录及其子目录中的所有文件和目录
            index = self._json_load()

            added_count = 0
            
            for item in full_path.rglob('*'):
                if item.is_file():
                    if {'.pygit', '.git'} & set(item.relative_to(full_path).parts):
                        # 跳过 .pygit / .git 目录中的文件
                        continue
                    # 以字节形式读取文件中数据
                    file_content = item.read_bytes()
                    # 根据 file_content 创建 BLOB 对象并将其存储在 .pygit/objects 目录中
                    blob = Blob(file_content)
                    blob_hash = self._store_object(blob)
                    # 更新 index 文件，将文件路径和对应的 BLOB 哈希值添加到索引中
                    index[str(item.relative_to(self.path))] = blob_hash

                    added_count += 1
                    print(f"Added file '{item.relative_to(self.path)}' to staging area with hash {blob_hash}.")

            self._save_index(index)

            if added_count > 0:
                print(f"Added {added_count} files from directory '{full_path.relative_to(self.path)}' to staging area.")
            else:
                print(f"Directory {dir_path} is already up to date.")

    def commit(self, arg1, author = 'PyGit user <user@kosmigen.com>'):
        """提交暂存区的更改到仓库"""

        
    def _store_object(self, git_object: GitObject) -> str:
        """将 Git 对象存储在 .pygit/objects 目录中"""
        obj_hash = git_object.hash()
        obj_path = self.objects_dir / obj_hash[:2] / obj_hash[2:]  

        # 创建对象存储路径的父目录（如果不存在）
        obj_path.parent.mkdir(parents=True, exist_ok=True)
        # 将序列化后的对象写入文件
        obj_path.write_bytes(git_object.serialize())

        return obj_hash

    def _json_load(self) -> dict[str, str]:
        """从 JSON 文件中加载数据"""
        if not self.index_file.exists():
            return {}
        try:
            return json.loads(self.index_file.read_text())
        except json.JSONDecodeError:
            return {}

    def _save_index(self, index: dict[str, str]):
        """将索引数据保存到 JSON 文件中"""
        try:
            self.index_file.write_text(json.dumps(index, indent=2))
        except OSError as e:
            raise ValueError(f"Error saving index file '{self.index_file}': {e}")