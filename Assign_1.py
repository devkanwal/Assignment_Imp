import collections
import csv
import sys

# Dictionary to store the file read
csv_cache = {}

# Cache Class 
class LRUCache:
    def __init__(self, capacity):

        # Initailizing the capacity of the cache
        self.capacity = capacity
        # Creating a dictionary for cache
        self.cache = collections.OrderedDict()
        # Creating a dictionary for storing the result in order
        self.OrderedResult = collections.OrderedDict()

    # Function to fetch the values from the cache for the given key
    def get(self, key):
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return -1

    # Function to set the values in cache for a key
    def set(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value
        
        print "Insert Key,Value: "+key+","+str(value)

        if(len(self.cache)>1):
            # Storing the data in the order of the key
            self.OrderedResult = collections.OrderedDict(sorted(self.cache.items(),key=lambda (key,value):key,reverse = True)) 

    # Function to delete the values in cache for a key
    def delete(self,key):
        try:
            self.cache.pop(key)
        except KeyError:
            return -1

    # Function to update the values in cache for a key
    def update(self,key,value):
        try:
            self.cache[key] = value
        except KeyError:
            return -1

    # Function to write cache values into a file
    def store_in_csv(self):
        with open('Cache Result.csv','wb') as csv_file:
            writer = csv.writer(csv_file)
            for key,value in self.OrderedResult.items():
                writer.writerow([key,value])


def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=',')
    for row in reader:
        if row['Marks obtained'] in csv_cache:
            csv_cache[row['Marks obtained']].append(row['Name'])
        else:
            csv_cache[row['Marks obtained']] = [row['Name']]
            csv_cache[row['Marks obtained']].append(row['Class Enrolled'])
            csv_cache[row['Marks obtained']].append(row['ID'])

def main():

    # Reading CSV file
    with open("StudentData.csv") as f_obj:
        csv_dict_reader(f_obj)

    # Define Cache Size
    new_cache = LRUCache(30)

    # Reading values from file to cache
    for key in sorted(csv_cache.iterkeys(),reverse=True):
        new_cache.set(key,csv_cache[key])
    
    # Insert New Value to the Cache
    new_cache.set('26',['Kanwal','Engineer','21'])
    new_cache.set('56',['Captain America','Avenger','22'])
    new_cache.set('75',['Iron Man','Rockstar','23'])
    new_cache.set('96',['Hulk','Scientist','24'])
    new_cache.set('58',['Deadpool','Comic','25'])
    new_cache.set('84',['Thor','Other World','26'])
    
    # Reading values from cache giving specified key
    inserted_val =  new_cache.get('40')
    print inserted_val
    
    # Delete a particular key
    new_cache.delete('40')
    inserted_val =  new_cache.get('40')
    # Returns -1 as the key is not present
    print inserted_val

    # Update Value for the given key
    new_cache.update('84',['Dr Who','Sorcerous','26'])
    inserted_val =  new_cache.get('84')
    print inserted_val

    print "Exiting..... Data Stored in a file"
    
    # Store the value in file
    new_cache.store_in_csv()

if __name__ == '__main__':
    
    # Loading the Main function
    main()

    # Initialising the values to be used only utf-8 format
    reload(sys)
    sys.setdefaultencoding('utf8')