import argparse
import sys
from object import GitRepository


    
def main():
    argparser = argparse.ArgumentParser(description="PyGit - A simple Git implementation in Python")
    sub_argparser = argparser.add_subparsers(dest="command", help="Available commands")

    # init command implementation
    init_parser = sub_argparser.add_parser("init", help="Initialize a new Git repository")
    init_parser.add_argument("path", nargs="?", default=".", help="Path to initialize the repository (default: current directory)")

    # add command implementation
    add_parser = sub_argparser.add_parser("add", help="Add files and directories to the staging area")
    add_parser.add_argument("paths", nargs="+", help="Files or directories to add")

    # commit command implementation
    commit_parser = sub_argparser.add_parser("commit", help="Commit changes to the repository")
    commit_parser.add_argument("-m", "--message", required=True, help="Commit message")
    commit_parser.add_argument("--author", help="Author of the commit (default: current user)")

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

    # 如果是 init 命令，则使用提供的路径初始化仓库，否则使用当前目录
    repo = GitRepository(args.path if args.command == "init" else ".")
    try:
        if args.command == "init":
            if not repo.init():
                print(f"Repository already exists in {repo.pygit_dir}.")
                return 
        
        elif args.command == "add":  
            if not repo.pygit_dir.exists():
                print(f"Error: No PyGit repository found in {repo.path}. Please run 'init' first.")
                return      

            # 遍历所有提供的路径并添加到暂存区
            # print(args.paths)
            # TODO: 如果文件修改，不会进行垃圾回收，暂存区会一直保存旧的文件内容，导致占用空间过大
            for path in args.paths: 
                full_path = repo.path / path
                if full_path.is_file():
                    repo.add_file(full_path)
                elif full_path.is_dir():
                    repo.add_directory(full_path)
                else:
                    raise FileNotFoundError(f"Path '{full_path}' does not exist.")
                
        elif args.command == "commit":
            if not repo.pygit_dir.exists():
                print(f"Error: No PyGit repository found in {repo.path}. Please run 'init' first.")
                return  
            repo.commit(args.message, author=args.author)
            
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}")
        sys.exit(1)
    

main()