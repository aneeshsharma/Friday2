import time


class Queue:
    def __init__(self):
        self.queue = []
        self.count = int(time.time() * 1000)

    def add(self, item):
        assert type(item) == dict
        id = self.count
        self.count += 1
        item['id'] = id
        item['taken'] = False
        item['completed'] = False
        self.queue.append(item)
        return id

    def find(self, id):
        start = 0
        end = len(self.queue) - 1
        while start <= end:
            mid = int((start + end) / 2)
            if self.queue[mid]['id'] == id:
                return self.queue[mid], mid
            elif self.queue[mid]['id'] < id:
                start = mid + 1
            else:
                end = mid - 1
        return None, -1

    def get_unprocessed(self):
        result = []
        for item in self.queue:
            if not item['taken']:
                result.append(item)
                item['taken'] = True
        return result

    def complete(self, id):
        item, index = self.find(id)
        assert item != None
        item['completed'] = True
        return item

    def delete(self, id):
        item, index = self.find(id)
        del self.queue[index]
        return item

    def delete_if_complete(self, id):
        item, index = self.find(id)
        if item['completed']:
            del self.queue[index]
            return item
        else:
            return None
