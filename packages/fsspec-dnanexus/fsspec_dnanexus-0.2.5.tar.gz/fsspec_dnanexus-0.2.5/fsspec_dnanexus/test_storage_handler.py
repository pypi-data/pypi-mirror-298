class DXStorageHandler:
    def __init__(self, base_path, handler):
        self.base_path = base_path
        self.handler = handler

    def __getattr__(self, name):
        def method(*args, **kwargs):
            if args:
                new_args = (self.base_path + args[0],) + args[1:]
            else:
                new_args = args
            return getattr(self.handler, name)(*new_args, **kwargs)
        return method

# Example handler class to demonstrate how RoutedHandler works
class ExampleHandler:
    def process(self, path, *args):
        print(f"Processing {path} with arguments: {args}")

# Example usage
base_path = "/base/path/"
handler = ExampleHandler()
routed_handler = DXStorageHandler(base_path, handler)

# This will call ExampleHandler.process("/base/path/some/path", arg1, arg2)
routed_handler.process("some/path", "arg1", "arg2")