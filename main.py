import server

def main():
    s = server.DHCPServer()
    try:
        s.listen()
    except KeyboardInterrupt:
        pass
    finally:
        s.process = False
        s.shutdown()

if __name__ == '__main__':
    main()
