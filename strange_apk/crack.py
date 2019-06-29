from base64 import b64decode

left = b64decode('c2N0ZntXM2xjMG1l')
right = '~8t808_8A8n848r808i8d8-8w808r8l8d8}8'[::2]

print left+right
