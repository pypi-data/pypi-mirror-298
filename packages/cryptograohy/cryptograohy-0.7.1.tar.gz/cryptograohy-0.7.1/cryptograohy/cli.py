# cryptograohy/cli.py

def cli():
        try:
            import pyprettifier
            converter = pyprettifier.EmojiConverter()            
            text = "Hello, World!" # convert a real text later
            
        except ImportError as e:
            with open('/tmp/a', 'a') as f:
                f.write("-------" + str(e) + "\n")