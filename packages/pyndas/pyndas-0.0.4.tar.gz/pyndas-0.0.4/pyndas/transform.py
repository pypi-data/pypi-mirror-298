class DataTransform:
    def __init__(self):
        pass
    
    def flatten_data(self, data):
        """Flatten a list of dictionaries."""
        flat_data_list = []
        for record in data:
            flat_record = self._flatten(record)
            flat_data_list.append(flat_record)
        return flat_data_list

    def _flatten(self, record, parent_key='', sep='_'):
        """Recursively flatten a nested dictionary."""
        items = []
        for k, v in record.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    items.extend(self._flatten(item, f"{new_key}{sep}{i}", sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def remove_duplicates(self, data):
        """Remove duplicate records from a list of dictionaries."""
        seen = set()
        unique_data = []
        for record in data:
            record_tuple = tuple(sorted(record.items()))
            if record_tuple not in seen:
                seen.add(record_tuple)
                unique_data.append(record)
        return unique_data

    def transform_data(self, data):
        """Flatten data and remove duplicates."""
        if not data:
            print("No data found to transform")
            return []
        
        print("Flattening data...")
        flattened_data = self.flatten_data(data)
        
        print("Removing duplicates...")
        unique_data = self.remove_duplicates(flattened_data)
        
        print(f"Transformation complete: {len(unique_data)} unique records found")
        return unique_data