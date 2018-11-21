'''Controller -> OUT TO BOTH R & S'''
#!/usr/bin/env python
import socket

TYPE = 0
CODE = 1
DATA = 2

def main():
    ''' controller request list from server, send selection to renderer'''
    addr = '10.0.0.1'
    server_port = 5300
    server_out_socket = create_sender_socket(addr, server_port)
    render_port = 5400
    render_out_socket = create_sender_socket(addr, render_port)
    controller(server_out_socket, render_out_socket)
    #disconnect_renderer(render_out_socket)
    #render_out_socket.close()
    disconnect_server(server_out_socket)
    server_out_socket.close()


def create_sender_socket(addr, port):
    '''create, connect, return socket sending to certain ip'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, port))
    return sock


def controller(server_out_socket, render_out_socket):
    '''Given server, and renderer, work with both'''
    selected_index = 0
    while True:
        media_list = get_list_from_server(server_out_socket)
        selected_index = request_choice_from_user(media_list)
        if selected_index == '-1':
            break
        # send selection to R
        else:
            busy = True
            # TODO: check if renderer is busy
            if not busy:
                selected_name = media_list[selected_index]
                send_choice_to_renderer(selected_name, render_out_socket)


def get_list_from_server(sock):
    '''GET media list from server'''
    print 'Requesting list from server'
    sock.send('1;0;')
    buffer_size = 1024
    print 'Receiving list from server'
    response = sock.recv(buffer_size).split(';')
    if response[TYPE] == '0':
        return []
    elif response[TYPE] == '2':
        media_list = response[DATA].translate(None, '[]')
        media_list = media_list.split(',')
        return media_list


def print_list(lst):
    '''Print list and indices to user'''
    index = 0
    for entry in lst:
        print str(index) + ': ' + entry
        index += 1


def request_choice_from_user(lst):
    '''Print list, get and validate user input, return choice '''
    print_list(lst)
    choice = raw_input('Select an option (or -1 to exit):')
    while (choice != '-1' and not choice.isdigit()) or (int(choice) \
        >= len(lst) or int(choice) < -1):
        choice = raw_input('Invalid input, try again: ')
    return choice


def send_choice_to_renderer(filename, sock):
    '''Send media choice to renderer'''
    message = '10;0;' + filename
    sock.send(message)

# TODO 
def send_playback_command(sock):
    '''PLAY, PAUSE, ETC. RELAY TO RENDERER'''
    return sock


def disconnect_server(sock):
    '''Send message to terminate connection to S'''
    message = '3;0;'
    sock.send(message)

def disconnect_renderer(sock):
    '''Send message to terminate connection to R'''
    message = '18;0;'
    sock.send(message)


main()
