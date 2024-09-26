class DataTransform:
    def flatten_data(self, data):
        flat_data = {}
        for record in data:
            flat_data = self._flatten(record)
            flat_data.append(flat_record)
        return flat_data

        for key, value in data.items():
            if isinstance(value, dict):
                flat_data.update(self.flatten_data(value))
            else:
                flat_data[key] = value
        return flat_data
    
    def _flatten(self, record, parent_key='', sep='_'):
        """nested dictionary."""
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
        seen = set()
        unique_data = []
        for record in data:
            record_tuple = tuple(sorted(record.items()))
            if record_tuple not in seen:
                seen.add(record_tuple)
                unique_data.append(record)
        return unique_data