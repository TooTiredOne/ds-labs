from multiprocessing import Pipe, Process


def local_time(counter):
    return f"VECTOR_TIME={counter}"


def calc_recv_timestamp(recv_timestamp, counter):
    counter = [max(recv_timestamp[i], counter[i]) for i in range(len(counter))]
    return counter


def event(pid, counter):
    counter[pid] += 1
    print(f"Something happend in {pid}   {local_time(counter)}")
    return counter


def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Some message', counter))
    print(f'Message sent from {pid}    {local_time(counter)}')
    return counter


def recv_message(pipe, pid, counter):
    message, time_stamp = pipe.recv()
    counter = calc_recv_timestamp(time_stamp, counter)
    counter[pid] += 1
    print(f'Message received at {pid}    {local_time(counter)}')
    return counter


def process_one(pid, a_b,):
    counter = [0, 0, 0]
    counter = send_message(a_b, pid, counter)
    counter = send_message(a_b, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(a_b, pid, counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recv_message(a_b, pid, counter)
    print(f'a:  {counter}')


def process_two(pid, b_a, b_c):
    counter = [0, 0, 0]
    counter = recv_message(b_a, pid, counter)
    counter = recv_message(b_a, pid, counter)
    counter = send_message(b_a, pid, counter)
    counter = recv_message(b_c, pid, counter)
    counter = event(pid, counter)
    counter = send_message(b_a, pid, counter)
    counter = send_message(b_c, pid, counter)
    counter = send_message(b_c, pid, counter)
    print(f'b:  {counter}')


def process_three(pid, c_b):
    counter = [0, 0, 0]
    counter = send_message(c_b, pid, counter)
    counter = recv_message(c_b, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(c_b, pid, counter)
    print(f'c:  {counter}')


if __name__ == '__main__':
    a_b, b_a = Pipe()
    b_c, c_b = Pipe()

    process1 = Process(target=process_one,
                       args=(0, a_b))
    process2 = Process(target=process_two,
                       args=(1, b_a, b_c))
    process3 = Process(target=process_three,
                       args=(2, c_b))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
