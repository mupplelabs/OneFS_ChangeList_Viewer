import json
import random
import time

def generate_large_demo(num_entries=1000):
    entries = []
    
    # Base timestamp
    base_time = int(time.time()) - (86400 * 7) # 1 week ago
    
    directories = [
        "/ifs/data/marketing",
        "/ifs/data/engineering",
        "/ifs/data/sales",
        "/ifs/data/hr",
        "/ifs/home/users",
        "/ifs/archives/2023",
        "/ifs/archives/2024",
        "/ifs/system/logs"
    ]
    
    file_extensions = [".txt", ".pdf", ".docx", ".xlsx", ".csv", ".mp4", ".jpg", ".png", ".log", ".bin", ".dat", ".conf"]
    
    change_types_pool = [
        "ENTRY_MODIFIED",
        "ENTRY_ADDED",
        "ENTRY_HAS_ADS",
        "ENTRY_ADS",
        "ENTRY_PATH_LOOKUP_REQ",
        "ENTRY_HAS_HARDLINKS",
        "ENTRY_WORM_COMMITTED"
    ]
    
    current_lin = 4200000000
    current_id = 68000000000
    
    def get_time():
        return {"nsec": 0, "sec": base_time + random.randint(0, 86400 * 7)}
    
    i = 0
    while len(entries) < num_entries:
        entry_type = random.choices(
            ['regular_add', 'regular_mod', 'directory_mod', 'remove', 'move'],
            weights=[30, 40, 10, 10, 10], k=1
        )[0]
        
        lin = current_lin + i
        item_id = str(current_id + i)
        parent_lin = current_lin - random.randint(100, 1000)
        
        dir_path = random.choice(directories)
        filename = f"file_{i}{random.choice(file_extensions)}"
        path = f"{dir_path}/{filename}"
        
        size = random.randint(0, 1073741824 * 2) # up to 2GB
        phys_size = size + random.randint(0, 4096)
        
        base_entry = {
            "atime": get_time(),
            "btime": get_time(),
            "ctime": get_time(),
            "mtime": get_time(),
            "data_pool": -3,
            "metadata_pool": -3,
            "gid": random.choice([0, 1000, 1001, 1002]),
            "uid": random.choice([0, 1000, 1001, 1002]),
            "id": item_id,
            "lin": lin,
            "parent_lin": parent_lin,
            "physical_size": phys_size,
            "size": size,
            "user_flags": ["inherit", "writecache", "wcinherit"]
        }
        
        if entry_type == 'regular_add':
            entries.append({
                **base_entry,
                "file_type": "regular",
                "path": path,
                "change_types": ["ENTRY_ADDED"] + random.sample(change_types_pool, random.randint(0, 2))
            })
            
        elif entry_type == 'regular_mod':
            entries.append({
                **base_entry,
                "file_type": "regular",
                "path": path,
                "change_types": ["ENTRY_MODIFIED"] + random.sample(change_types_pool, random.randint(0, 2))
            })
            
        elif entry_type == 'directory_mod':
            entries.append({
                **base_entry,
                "file_type": "directory",
                "path": dir_path,
                "change_types": ["ENTRY_MODIFIED"],
                "size": random.randint(1024, 8192),
                "physical_size": random.randint(1024, 8192)
            })
            
        elif entry_type == 'remove':
            entries.append({
                **base_entry,
                "file_type": "(REMOVED)",
                "path": path,
                "change_types": ["ENTRY_REMOVED"],
                "id": f"230584307{item_id}" # Removed IDs are often larger
            })
            
        elif entry_type == 'move':
            # Create the paired remove/add entries required by the API for a rename/move
            old_filename = f"old_file_{i}{random.choice(file_extensions)}"
            new_filename = f"new_file_{i}{random.choice(file_extensions)}"
            
            common_time = get_time()
            
            # Removed half
            entries.append({
                **base_entry,
                "mtime": common_time,
                "ctime": common_time,
                "file_type": "(REMOVED)",
                "path": f"{dir_path}/{old_filename}",
                "change_types": ["ENTRY_REMOVED", "ENTRY_PATH_CHANGED"],
                "id": f"230584307{item_id}"
            })
            
            # Added half
            entries.append({
                **base_entry,
                "mtime": common_time,
                "ctime": common_time,
                "file_type": "regular",
                "path": f"{dir_path}/{new_filename}",
                "change_types": ["ENTRY_ADDED", "ENTRY_PATH_CHANGED"] + random.sample(change_types_pool, random.randint(0, 1))
            })
            
        i += 1

    # Shuffle so it's not totally ordered
    random.shuffle(entries)
    
    # Cap strictly to requested size just in case the move generator pushes it slightly over
    entries = entries[:num_entries]
    
    print(f"Generated {len(entries)} entries. Writing to large_changelist_demo.json")
    
    with open('large_changelist_demo.json', 'w') as f:
        json.dump({"entries": entries}, f, separators=(',', ':'))

if __name__ == "__main__":
    generate_large_demo(1000)
