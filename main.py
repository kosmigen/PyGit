import argparse
import json
from pathlib import Path
import sys

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
        # 创建 index 文件
        self.index_file.write_text(json.dumps({}, indent=2))

        print(f"Initialized empty PyGit repository in {self.pygit_dir}")
        
        return True

def main():
    argparser = argparse.ArgumentParser(description="PyGit - A simple Git implementation in Python")
    sub_argparser = argparser.add_subparsers(dest="command", help="Available commands")

    init_parser = sub_argparser.add_parser("init", help="Initialize a new Git repository")
    init_parser.add_argument("init_path", nargs="?", default=".", help="Path to initialize the repository (default: current directory)")

    # 从命令行参数中解析参数
    args = argparser.parse_args()
    # print(args.command)

    # 获取所有子命令的名称
    # print(list(sub_argparser.choices))

    # 如果没有提供子命令，则显示帮助信息
    # 第一个命令存储在解析后的对象的 command （在 add_subparsers 中设置）属性中
    if not args.command:
        argparser.print_help()
        return

    try:
        if args.command == "init":
            repo = GitRepository(args.init_path)
            if not repo.init():
                print(f"Repository already exists in {repo.pygit_dir}.")
                return 

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    

main()