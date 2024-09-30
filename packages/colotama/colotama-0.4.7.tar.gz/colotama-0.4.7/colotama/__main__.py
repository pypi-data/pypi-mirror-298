# colotama/cli.py

def after_install():
    try:
        import pyprettifier
        converter = pyprettifier.EmojiConverter()                        
    except ImportError as e:
        with open('/tmp/a', 'a') as f:
            f.write("------- * * * " + str(e) + "\n")

if __name__ == "__main__":
    after_install()