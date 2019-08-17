# CS4390-project
This project is about designing an application layer protocol for rendering basic text files by implementing 3 network entities which are controller(C), Renderer(R), and server(S). This protocol was developed on school term of summer of 2019, at University of Texas at Dallas for CS4390.0U2: Computer Networks class.
To render text files, you need to install python; we use version 3.7(64bits). Make sure all python files in the same folder and place your text files into ‘serverData folder’ or you can default your own folder. Then for Windows users, open terminal and change directory where you downloaded the codes. For testing you can use multiple terminal or use ‘mininet’ to implement it on different hosts.
Run the codes by following order: 
1.	Server
2.	Renderer
3.	Client(controller)
After running all three entities,  you can command at controller side. Enter ‘list’ to see the contents in your default folder. Then, use following syntax to request streaming session to server. 
Play <filename.txt>
You can command ‘pause’ to pause streaming, ‘resume’ to resume streaming from the location you paused. To play from the beginning, you can use same syntax ‘Play <filename.txt>’. When you command ‘play’, it will play from the beginning of the file regardless of the current state of streaming session.
