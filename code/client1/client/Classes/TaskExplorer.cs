using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Controls;
using System.Net.Sockets;

namespace client
{
    class TaskExplorer
    {
        private TcpClient client;
        private string authToken;

        public TaskExplorer(TcpClient _client, string _token)
        {
            client = _client;
            authToken = _token;
        }

        /// <summary>
        /// Delets the node
        /// throws exception if sth goes wrong
        /// </summary>
        /// <param name="node">node to delete</param>
        public void deleteTask(TreeViewItem node, TreeView tree)
        {
            Task task = node.Tag as Task;
            if (task == null)  // every node should have Task tag!
                throw new Exception();

            NetworkStream stream = client.GetStream();
            Protocol.sendToServer(stream,
                Protocol.getPacketDeleteTask(task.id, authToken));
            PacketSTC response = Protocol.recieveFromServer(stream);
            checkDeleteTask(response, node, tree);
        }

        /// <summary>
        /// Adds a new root task
        /// throws exceptions if sth goes wrong
        /// </summary>
        /// <param name="description"></param>
        public TreeViewItem addNewTask(string description, string name,
             TreeView tree)
        {
            NetworkStream stream = client.GetStream();
            Protocol.sendToServer(stream,
                Protocol.getPacketAddTask(-1, description, authToken));

            PacketSTC response = Protocol.recieveFromServer(stream);
            return checkAddNewTask(response, description, name, tree);
        }

        /// <summary>
        /// Adds a new subtask
        /// throws exception if sth goes wrong
        /// </summary>
        /// <param name="description"></param>
        /// <param name="name"></param>
        /// <param name="parentId"> parents id</param>
        /// <param name="authToken"></param>
        /// <param name="parentNode">parents node in treeView</param>
        public TreeViewItem addNewSubTask(string description, string name, 
            int parentId,  TreeViewItem parentNode)
        {
            NetworkStream stream = client.GetStream();
            Protocol.sendToServer(stream,
                Protocol.getPacketAddTask(parentId, description, authToken));

            PacketSTC response = Protocol.recieveFromServer(stream);
            return checkAddNewSubtask(response, description, name, parentNode, parentId);
        }

        public void updateTask(int id, int parentId, string description,
            string name, TreeViewItem node)
        {
            Console.WriteLine("w update task explorer, przed wyslaniem do serwera");
            NetworkStream stream = client.GetStream();
            Protocol.sendToServer(stream,
                Protocol.getPacketUpdateTask(id, parentId, name,
                description, authToken));
            PacketSTC response = Protocol.recieveFromServer(stream);
            checkUpdateTask(response, name, description, node);
        }


        // adds new node to the treeView
        public TreeViewItem addNewTaskToTreeView(Task task, TreeView tree)
        {
            TreeViewItem root = new TreeViewItem() { Header = task.name };
            root.Tag = task;
            tree.Items.Add(root);
            return root;
        }

        // adds new child to the node in the treeView
        public TreeViewItem addNewSubtaskToTreeView(Task task, TreeViewItem node)
        {
            TreeViewItem child = new TreeViewItem() { Header = task.name };
            child.Tag = task;
            node.Items.Add(child);
            return child;
        }

        public Task getTask(int id, int parent, string name,
            string description, string createOn)
        {
            Task t = new Task();
            t.id = id;
            t.parent = parent;
            t.name = name;
            t.description = description;
            t.lastChange = createOn;
            t.createOn = createOn;
            t.done = false;

            return t;
        }


        // **************** CHECKING FUNCTIONS *********** //
        // *********************************************** //
        // Check whether everything went OK
        // throw Exception if sth went wrong

        private TreeViewItem checkAddNewTask(PacketSTC serverResponse, string description,
            string name, TreeView tree)
        {
            if (serverResponse.type.Equals(Protocol.ADD_TASK_OK))
            {
                Task newTask = getTask(Convert.ToInt32(serverResponse.parameters["id"]),
                    -1, name, description, (string) serverResponse.parameters["createdOn"]);

                return addNewTaskToTreeView(newTask, tree);
            }
            else
            {
                throw new couldNotAddNewTask();

            }
        }

        // like checkAddNewTask but invokes
        // different function inside:  addNewSubtaskToTreeView(newTask, parentNode)
        // It needs TreeViewItem instead of TreeView!
        private TreeViewItem checkAddNewSubtask(PacketSTC serverResponse, string description,
            string name, TreeViewItem parentNode, int parentId)
        {
            if (serverResponse.type.Equals(Protocol.ADD_TASK_OK))
            {
                Task newTask = getTask(Convert.ToInt32(serverResponse.parameters["id"]), parentId,
                    name, description, (string) serverResponse.parameters["createdOn"]);

                return addNewSubtaskToTreeView(newTask, parentNode);
            }
            else
            {
                throw new couldNotAddNewTask();
            }
        }

        private void checkDeleteTask(PacketSTC serverResponse, TreeViewItem node, TreeView tree)
        {
            string type = serverResponse.type;

            if(type.Equals(Protocol.DELETE_TASK_OK))
            {
                tree.Items.Remove(node);
                foreach (TreeViewItem item in tree.Items)
                {
                    deleteRecursive(item, node);
                }
            }
            if (type.Equals(Protocol.DELETE_TASK_FAILED))
            {
                //TODO
            }
            if (type.Equals(Protocol.OPERATION_NOT_ALLOWED))
            {
                //TODO
            }
            if (type.Equals(Protocol.AUTHENTITACION_REQUIRED))
            {
                //TODO
            }
        }

        private void deleteRecursive(TreeViewItem node, TreeViewItem nodeToDelete)
        {
            node.Items.Remove(nodeToDelete);
            foreach (TreeViewItem n in node.Items)
                deleteRecursive(n, nodeToDelete);
        }

        private void checkUpdateTask(PacketSTC serverResponse,
            string name, string description, TreeViewItem node)
        {
            string type = serverResponse.type;
            if( type == Protocol.UPDATE_TASK_OK )
            {
                Console.WriteLine("update task OK");
                Task t = node.Tag as Task;
                t.name = name;
                t.description = description;
                node.Header = t.name;
                node.Tag = t;
                
            }
            else
            {
                Console.WriteLine("update task FAILED");
            }
                
        }
    }
}