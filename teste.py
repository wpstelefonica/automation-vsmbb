script = '{"query":"\\nSELECT\\n  \\"sig_regional\\"\\nFROM \\"celulas\\"\\nWHERE \\"__time\\" BETWEEN TIMESTAMP \'2024-11-16 00:00:00\' AND TIMESTAMP \'2002-11-17 23:59:59\'\\nGROUP BY \\"sig_regional\\"\\n","context":{}}'
model = '{"query":"\\nSELECT\\n  \\"sig_regional\\"\\nFROM \\"celulas\\"\\nWHERE \\"__time\\" BETWEEN TIMESTAMP \'2024-11-16 00:00:00\' AND TIMESTAMP \'2024-11-17 23:59:59\'\\nGROUP BY \\"sig_regional\\"\\n","context":{}}'

import os

user_profile = os.getenv("USERPROFILE")
downloads_path = os.path.join(user_profile, "Downloads")
full_path = os.path.join(downloads_path)

print(full_path)

onedrive = os.getenv("ONEDRIVE")
downloads_path = os.path.join(user_profile, "Downloads")
full_path = os.path.join(downloads_path)

print(onedrive)
