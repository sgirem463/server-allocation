# Server name allocation service
# There can be many different server types, e.g. database, web, api,
# A server name is server type + id, e.g. web1, database23, api32
# each allocation should return name with the lowest avaliable id, starting from 1
#
# The service supports deallocation when a server is no longer needed, its id should
# be return to the pool for future allocation
# The system should be able to detect deallocation with an invalid id, i.e. id that
# hasn't been allocated
#
#
# A few thoughts:
# 1. Each server type should maintian its own id space
# 2. allocate and return the lowest available id for each server type
# 3. A returned server id is available for allocation, the system should return False
#    if an invalid id is deallocated.
# (3) implies the system should keep track of ids allocatiioed for each server type
#
# the requirement to return the lowest available id indicates a heap is prbably
# a good candidate for maintaining the id.
#
# if there is a limit on the number of each server type available, we can use a
# heap to keep ids for each server type with reasonably efficient time complexity
# However whhen the number of servers is unlimited, we cannot keep a heap of
# unlimited size
#
# We need to be able to find the lowest available id efficiently no matter
# there are deallocated ids or not
# =>
# when there is no deallocated id, need to get the next lowest id
# when there are deallocated ids, need to get the lowest of the deallocated ids
#
# one way is to maintain a nextid for each server type
#
# However a heap is not efficient for member check (for deallocation vallidation),
# a set is good choice for keeping track of allocated ids, on top of that a heap
# is used keep track of returned ids
#


from collections import defaultdict
import heapq

class Servers:
    def __init__(self):
        self.used = defaultdict(set) # indexed by the server type
        self.returned = defaultdict(list) # each server type keeps a heap


    def allocate(self, name):
        if not self.returned[name]:
            id = len(self.used[name]) + 1
            self.used[name].add(id)
        else:
            id = heapq.heappop(self.returned[name])
            self.used[name].add(id)
        return name + str(id)
            

    def deallocate(self, name, id):
        if id not in self.used[name]:
            return False
        heapq.heappush(self.returned[name], id)
        self.used[name].remove(id)
        return True
        



Servers = Servers()

print(Servers.allocate('web'))  # web 1
print(Servers.allocate('web'))  # web 2
print(Servers.allocate('web'))  # web 3
print(Servers.allocate('web'))  # web 4
print(Servers.allocate('web'))  # web 5
print(Servers.allocate('web'))  # web 6
print(Servers.deallocate('api', 1))  # False

print(Servers.allocate('api'))  # api 1
print(Servers.allocate('api'))  # api 2
print(Servers.allocate('web'))  # web 7
print(Servers.allocate('web'))  # web 8
print(Servers.allocate('web'))  # web 9
print(Servers.allocate('api'))  # api 3
print(Servers.deallocate('fake', 2))  # False


print(Servers.allocate('web'))  # web 10
print(Servers.allocate('web'))  # web 11
print(Servers.deallocate('api', 1)) # api 1 

print(Servers.deallocate('web', 2)) # del web 2
print(Servers.allocate('api'))  # api 1
print(Servers.deallocate('api', 88))  # False

print(Servers.allocate('web'))      # web 2
print(Servers.deallocate('web', 8)) # del web 8
print(Servers.deallocate('web', 5)) # del web 5
print(Servers.deallocate('web', 1)) # del web 1
print(Servers.allocate('web')) # web 1
print(Servers.allocate('web')) # web 5
print(Servers.allocate('api')) # api 4
print(Servers.allocate('web')) # web 8
print(Servers.deallocate('web', 1)) # del web 1
print(Servers.deallocate('web', 2)) # del web2 
print(Servers.deallocate('web', 3)) # del web 3
print(Servers.deallocate('web', 1)) # False

