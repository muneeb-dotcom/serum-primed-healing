import socket
print(socket.gethostbyname("pubchem.ncbi.nlm.nih.gov"))
s = socket.create_connection(("pubchem.ncbi.nlm.nih.gov", 443), timeout=10)
print("connected OK")
s.close()