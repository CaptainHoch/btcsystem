import msgpack
import socket
import select
import pickle
import os
import sys
import networkx as nx
from random import randint

sys.path.insert(0, os.getcwd()+'\\my modules')
bad_list = [u'18ZRV3UyJVD28Sob7Wp82vbfMejxvFWnxZ', u'13D5suFKGj6ypXL3pWr8SPXqPdCq9ZPxEn', u'17b9E1XWKhYPL3ceFDSyQYhGvpyMxaHyez', u'19tHssV5e3Uvq8X9DYJaP5b8k3yTJCCKWN', u'17wBq55Y1A5qp4yupN2vnPPrpWfuXw9YbM', u'1CSAQR36BXPspfNkFSomw3KWJjTSxKfhgD', u'17UqbxfJEtEYkDmdHAmG7ohawsM47K8XJC', u'17SM6ow7QqyKc7aJFYGeFZEpJJfPtBcoCR', u'1BSmvEz17tN7ptJmFQn1Dup96chPwawiKN', u'1HRQU3eFLfucLrCtkJs5xSZbFETmdJB9TN', u'1N2VaTYZfYZdYQikwdLBUQh6eTEbDgsSfM', u'1QLModSmDrR1Rdc6b4bSGo3GtxirBAdNCh', u'13q5Xy5rJmNDD9Nkp4JJHGeBR72CZE8SXH', u'1QCK5QCLBvaBD7hydNCCSc6Kq73JCWtJUw', u'19UPynth1LPtX6NV8a7MyJFkV2w3HgG4a3', u'1FKwZUuDbHSim57LU7w6P85zGXPdUcs966', u'19qah9qS5H5MH7NFTjudchoSTV7bWB897e', u'1NMGeZ1GuvY3Nm7CF7NvuTLUCNbw8gmazZ', u'1E96AUN6LiZWaNWm7HZUZXqnp9BWSAWgd5', u'15cS588VeeLwiNPjKhnNBb4MCTHRA83dFz', u'1DwFrHf3T5MnVgtbbGTWFpECP1Hdg3C5oQ', u'1HeTes7YbkFQuD8oMjdduUgsLAu23EzSpj', u'18pjoST241mQFyTLpXqBCttAJ8bg1eTJvg', u'1Hv99X8ogNXGdcoLhgJeE9Z2nbnsXfBXM3', u'12tKcRFvHXuefwLVnj8Ea8bjbkjRfoPD51', u'1APe97yBtJrAR7Yz1mCJoMTgJG46ujUcSw', u'1mhTeiod2KuYCyA4ukk8GuZ9Z4rGsKKbs', u'1BhaQUdn4DTtzP2bXVsWehb8HaMuvguacJ', u'19scmZspmBznAGSY5JoLreHtx9vHNxDG2M', u'1PDjsEDTyh91ChLEdssESG8MoqHa4BwnqG', u'1NqYwi56TDQrq1i4FDdqX8TcoXvDtspMvc', u'148j79E78HJSd15F7NbT5wrwLgP7vZ5wDT', u'1BnTJCoN4YvK9WkHsP35BNJKcBkJbA9GrH', u'1BthrG5csBabyrh2MX89uZYhZ1w32e4TbR', u'1KnKGNRkPYrDwFbpuWqeWHcDLMNkcbAj8E', u'1Gw1gZNMTcAJQvZNDbpLrwjyCYBfphMpg4', u'122BQVJ56AnkRUmApx4Ae96YPDebW8AZPJ', u'1Jyt1UA21yXG3RZoJN2hhmE8CtR5eLG9wo', u'1KKr74ihoDvu25BDTGRzdraAvtvdgvoECt', u'1EDj7k136GAcQvkRRrZJNHKsGfRoJ6GdWd', u'1NB43hF1hz9sg8w28zBn19kFkjGGEnSZbY', u'14mVUrbQcGfATL7EQ84XhQFMoB141GWLbZ', u'1CUDd1fcaBmX3rTKrVQZFfueh2TuahWE6t', u'1PmvP8TuUKDo2caJMrBcjVuBkiNH7kxyTm', u'12BUpfRPNGJMYoMyCYKesjeGabLcqM8Eig', u'12BT2hTRYZU6MDWNZCVy7idbkXfb9ULqag', u'1dZ2N1ZQQJqzywvuBBAeMKpQBpeFPgQqt', u'1GygzPrubvTpT2LKRYyCV2Xv5sEGPebT8Y', u'1DaGVqhKNF57CS22AJ9Z2MeQsLtHdSjvZp', u'13cSbbidN5fE9YDWqJkSdTFRMsxu3e4evd', u'13PWMusAVuQCmocVAQc1pxvwX3YCb6j1sq', u'1NtjzvGCVE8NE7cyX6uh1acZimY81WcXbt', u'1KifvT1omGjVggSd93ecqVVg7uRy9bXUz6', u'1Eeuad7gM7HCHXiEmaWbwF5KE1DuHNo3tV', u'1HL6Ja1hbGBN4mkzFBXtQvm53LKzKtyMYx', '12JgZPRt4fAwgD7nBMAZxcJZBrFzraTAEV', u'1Wg3f5vC7NRBJ6W9zF5oFHdMdoRdLAcPH', u'1MPAGxS7MLKvJQXE1pd2Hh8fCF1rjtZ4Um', u'1JrbzHFQ6GfeCcmJCKkLe1ZD8LMk5dj7nx', u'1A63Lm8XY19hcjyCLcUtbvNg9wXVwrH9K1', u'1C6rBoAh9AtEkAfPXaiooNtFLAMiEnvmYH', u'1KnJRsbKL4mvXBdDAF6Av7r3ddxm5YUa37', u'1656xDWzwghNqfxYP3ws5wdLQvCcydSP9k', u'1N1B5SMSNAk8wzzLc9YLLgRAMGkprTYgfP', u'1KbgP5jzQpLu6ZwjMpBoh9yW2iDCQM1ipL', u'1NoVexYVYc1LRj37LkeD31DWDG9YY722bv', u'1JA8Fvj1QnxGniFnWoW3vhqy6ZVQUgxwbD', u'1KsZx7VAiE9gKauM8p7QyWKXe4aNZTcd21', u'15wY8BTyiX7pbzCRYEE2ZGGTHbPYNSh9wN', u'1VayNert3x1KzbpzMGt2qdqrAThiRovi8', u'1AmWW8zo3m7N3snQJwBC5tdndJTPks8wt7', u'1GWzd2pTvLg1TUFid8E6rr9yJPEuUK1MS', u'17RXV3S4ZmdyVSW42qAt6KJNsMVYnyZWYE', u'178HnWgA1KV1CWfZ8dcrjRcvwLMd1ueLrK', u'1C8DJTJsUVMxXH3yzQfH3EYoxbxEZwcCwF', u'1HpzYaE6yP6KQespCncEsRh5M9UVHfG8bW', u'1H3gJqwVDx9wNvZw5gaJekJyRiYerm8QjZ', u'1C4yJ32YCJPXmVLjzRjL4N7GGfVNQCPUdV', u'12xJkuaFzQDTokNr53kiDbK5KfoKYFrFix', u'1GRj6DPKS3F12sQBtTLPenidYxC8yNWbju', u'1JAZ9GFLaXNmafyGbb4qDnVqwexskiqgB8', u'1D2yZqSQXaJNZh3hd88zGnW71RwtQwA8Pp', u'1Li524GtkS2s1LEJYcJaLQWPKiv2oQRaGh', u'1D1wNY7KMuWaz4qSf9iFsPFKhasgYWtPZ7', u'1CejcRSiiiXTsJnMziGymqpiqbuqiK3S9b', u'1JiZiWuwqGbmshjGo2JbDzgbQUeSr7Ln5D', u'1McCWZqW9b4rpKmcqV4DSsRLmjq9nCNA9P', u'1MCoSNNSp3TLJhw7jdKbEyQYzKdeBWe6kL', u'1M7Xj8ujCT5fJwMqzTifNyPUCjq9bFcYg4', u'1GbxFuie7wkbcmLihpSt7yfH7tL4PYP8Gw', u'1MAGyD37jnbSuEB1R6vB4pT33omPPpdfr3', u'19ZwqqTrnE4sRfKeiWfnv29SzwN3RX6N31', u'1DgGFi8LKmkfd6WgLHreZPSk2g52dzRUoa', u'1Jaa5nFowdPdALNopkiHFYpobLbxD7zR4B', u'1ELpxqcD5ZvU46tQ1Kzh8XrokXpk9NbsJN', u'1BeuDMy5KgpLBGvCvjXijsTcfLfLgncs6g', u'1CtPRhjahQjichn3KZ83M1V1Gm17MnSABf', u'1ANKfEauNx6yfw7LFyvSznJh4zZZ18PqFu', u'13c9aoS71jT5Na1NLYDKWwNj1xVBt7j5t6', u'15zTsMpLQTXfqgVfzoXVHZfc1dgfZ7Aaxv', u'1FARsmcbXYK4vr9RimsHhTv4QEQZoZNL37', u'1Q3SmRhmjh6AK32B3uJjF8fJoF9xAUF1sk', u'18kdSc4kHH392yVJn6o9RA3BAqfGbuZQwW', u'18EJ3oj3Kwc2GovNX5C9Pa8sSeP1orM9sP']
bad_dict = {}
for address in bad_list:
    bad_dict[address] = randint(70, 90)

IP = "10.42.100.17"
PORT = 19704
LAST_CHARS = list(map(str, range(0, 10))) + list(map(chr, range(97, 123))) + \
             [chr(x) + 'c' for x in range(65, 91)]  # All available last characters

global my_socket
global handle_later
def pack_data(data, file):
    """
    Write to file with msgpack

    :param data: Data to write to file
    :param file: the file to write into
    """
    # lock.acquire()
    with open(file, 'wb') as outfile:
        msgpack.pack(data, outfile)
    # lock.release()


def unpack_data(file_name):
    """
    Read from file with msgpack

    :param file_name: the file to read from
    :return: return the data read
    """
    # lock.acquire()
    with open(file_name, "rb") as data_file:
        data = msgpack.unpack(data_file)
    # lock.release()
    return data


def handle_message(data):
    """
    handle a message received from the server
    :param data: the message the server sent
    :return: Nothing
    """
    global my_last_chars
    global my_address
    global unreceived_chars

    header = data[:3]  # divide data to header and message
    server_message = pickle.loads(data[3:], encoding='latin1')
    if header == b'1.4':
        # Server asked for information about wallet
        wallet_hash = server_message.encode()
        last_char = str(server_message[-1])
        if last_char.isupper():
            last_char += 'c'
        print("Wallet hash:", wallet_hash)
        # Get the dictionaries
        my_data_dict = unpack_data("data files/data_%s.msgpack" % last_char)
        my_data_dict = pickle.loads(my_data_dict, encoding='latin1')
        try:
            data_per_wallet = my_data_dict[wallet_hash]
        except KeyError:
            data_per_wallet = []
        print(data_per_wallet)
        answer = b'2.4' + pickle.dumps(data_per_wallet, 2)
        my_socket.send(answer)
    else:
        raise Exception('Got unknown message from server: {0} {1}'.format(header, server_message))


def get_facade_message():
    """
    Receive messages from other users via the server. Activated by thread.
    """
    global handle_later
    try:
        while True:
            for message in handle_later:
                handle_message(message)
                handle_later.remove(message)
            r_list, w_list, x_list = select.select([my_socket], [my_socket], [])
            if r_list:  # If server tries to send message
                print("rlist: ", r_list)
                data = my_socket.recv(4096)  # Get message
                print("Data:", data)
                if data and data != '[]':
                    handle_message(data)

    except (socket.error, select.error, ValueError) as error:
            raise error


def get_graph(address):
    last_char = address[-1]
    if last_char.isupper():
        last_char += 'c'
    my_socket.send(b'5.1' + pickle.dumps(address, 2))
    data = pickle.loads(my_socket.recv(16777216), encoding='latin1')
    print(data)
    wallet_info = data
    print("Information for wallet: " + address)
    print(wallet_info)
    data_per_wallet = wallet_info
    input_list = []
    output_list = []
    for wallet_data in data_per_wallet[0]:
        for tx in wallet_data:
            for tx_name, value in tx.items():
                input_list.append([value['input_addresses'], tx_name[0], value['value']])
                output_list.append([value['spent_tx_addresses'], value['spent_tx_hash'], value['value']])
    print(input_list)
    print(output_list)
    graph = nx.DiGraph()
    all_edges = []
    for input_info in input_list:
        try:
            for input_address in input_info[0]:
                all_edges.append(input_address)
        except TypeError:
            pass
    for output_info in output_list:
        try:
            for output_address in output_info[0]:
                all_edges.append(output_address)
        except TypeError:
            pass
    all_edges.append(address)
    all_edges = list(set(all_edges))
    print("All edges: ", all_edges)
    for x in all_edges:
        print(x)
        graph.add_node(x)

    for input_info in input_list:
        try:
            for input_address in input_info[0]:
                graph.add_edge(address, input_address)
        except TypeError:
            pass

    for output_info in output_list:
        try:
            for output_address in output_info[0]:
                graph.add_edge(output_address, address)
        except TypeError:
            pass

    for x in range(randint(1, 3)):
        graph.add_edge(all_edges[randint(0, len(all_edges) - 1)], all_edges[randint(0, len(all_edges) - 1)])
    print(graph)
    return graph


def graph_from_server(addr):
    address = addr
    graph = get_graph(addr)
    return graph


def setup_client():
    global my_socket
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.connect((IP, PORT))  # Connect to server
        my_socket.send(b'5.0' + pickle.dumps(True, 2))
        my_address = None
    except socket.error:
        print("Couldn't connect to server. Please try again later.")

