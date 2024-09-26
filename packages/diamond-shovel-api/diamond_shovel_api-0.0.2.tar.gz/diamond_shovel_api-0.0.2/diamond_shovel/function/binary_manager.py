class BinaryManager:
    def get_out_path_by_name(self, name: str):
        ...

    def register_binary_path(self, name: str, path: str):
        ...

    def execute_binary(self, name: str, cmd_args: list[str], timeout: int,
                       error_manage: bool = True, separate_output: bool = True, text: bool = True) \
            -> tuple[str | bytes, str | bytes]:
        ...

    def clear_outs_folder(self):
        ...

    def check_binary(self, name: str) -> bool:
        ...
