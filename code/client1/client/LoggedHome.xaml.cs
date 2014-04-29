using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

using System.Net.Sockets;
using Newtonsoft.Json;
using Microsoft.VisualBasic;

namespace client
{
    /// <summary>
    /// Interaction logic for LoggedHome.xaml
    /// </summary>
    public partial class LoggedHome : Window
    {
        private String username;
        private String token;
        private TcpClient client;

        //private List<Task> List<Task>;
        private TaskExplorer taskExplorer;

        public LoggedHome(string _username, string _token, TcpClient _client)
        {
            InitializeComponent();
            username = _username;
            token = _token;
            client = _client;
            taskExplorer = new TaskExplorer(_client, _token);
        }

        private void Grid_Loaded(object sender, RoutedEventArgs e)
        {
            List<Task> rootTasks = getChildren(-1);
            if(rootTasks != null)
               initTreeView(rootTasks);

            // TESTY
            Task t1 = new Task(); t1.name = "111";
            TreeViewItem node = 
                taskExplorer.addNewTaskToTreeView(t1, treeViewTaskExplorer);
            Task t2 = new Task(); t2.name = "222";
            TreeViewItem n1 =
                taskExplorer.addNewSubtaskToTreeView(t2, node);
            Task t3 = new Task(); t3.name = "333";
            TreeViewItem n2 =
                taskExplorer.addNewSubtaskToTreeView(t3, n1);
            taskExplorer.addNewSubtaskToTreeView(t3, n2);
            taskExplorer.addNewSubtaskToTreeView(t3, n2);

            addMenusToTreeExplorer();
        }

        // TESTY TESTY TESTY
        private void btnTest_Click(object sender, RoutedEventArgs e)
        {
            Packet p = new Packet();
            p.type = Protocol.ADD_TASK;
            p.parameters.Add("id", "mojeIDSUKO");
            List<Task>  lista = new List<Task>();
            Task t = new Task();
            t.description = "KSKAKSAKSKAKSAKA opis opis";
            lista.Add(t);
            p.parameters.Add("subtasks", lista);
            List<Task> listaZPOWROTEM = p.parameters["subtasks"] as List<Task>;
            if (listaZPOWROTEM == null)
                MessageBox.Show("listaZPOWROTEM null");
            string json = JsonConvert.SerializeObject(p);
            Console.WriteLine("{0}", json);
           
            Packet p2 = JsonConvert.DeserializeObject<Packet>(json);
            Console.WriteLine("TEST: p2.params[subtasks].description");
            //List<Task> l = p2.parameters["subtasks"] as List<Task>;
            //Console.WriteLine("{0}", l[0].description);
            //array.ToObject<List<SelectableEnumItem>>()
            Newtonsoft.Json.Linq.JArray jsonArray = (Newtonsoft.Json.Linq.JArray)p2.parameters["subtasks"];
            List<Task> l = jsonArray.ToObject<List<Task>>();
            Console.WriteLine("{0}", l[0].description);

            string json2 = JsonConvert.SerializeObject(p2);
            Console.WriteLine("{0}", json2);

        }

        // ***************** PRIVATE FUNCTIONS ************ //
        // ************************************************ //

        /// <summary>
        /// Initializes the treeView! adds all nodes
        /// </summary>
        /// <param name="List<Task>">root nodes!</param>
        private void initTreeView(List<Task> rootNodes)
        {
            foreach(Task rootTask in rootNodes)
            {
                TreeViewItem newRootNode = 
                    taskExplorer.addNewTaskToTreeView(rootTask, treeViewTaskExplorer);
                addSubtasks(newRootNode, rootTask.id);
            }
        }

        /// <summary>
        /// adds all subtasks to the parentNode
        /// </summary>
        /// <param name="parentNode">parent node in treeView</param>
        /// <param name="parentId">parents id</param>
        private void addSubtasks(TreeViewItem parentNode, int parentId)
        {
            List<Task> children = getChildren(parentId);
            if(children != null)
            {
                foreach(Task subtask in children)
                {
                    TreeViewItem subtaskNode = 
                        taskExplorer.addNewSubtaskToTreeView(subtask, parentNode);
                    // resursion!
                    addSubtasks(subtaskNode, subtask.id);
                }
            }
        }

        /// <summary>
        /// Returns chidlren of a parent as a List<Task> or null if sth wen wrong
        /// </summary>
        /// <param name="parentId"> parents id, use -1 to get root nodes </param>
        /// <returns> list of children </returns>
        private List<Task> getChildren(int parentId)
        {
            try
            {
                NetworkStream stream = client.GetStream();
                Packet packet = Protocol.getPacketSubtasks(parentId, token);
                Protocol.sendToServer(stream, packet);
                Packet response = Protocol.recieveFromServer(stream);

                // Changing p.parameters[subtasks] into List of Tasks
                Newtonsoft.Json.Linq.JArray jsonArray =
                    response.parameters["subtasks"] as Newtonsoft.Json.Linq.JArray;
                
                // we return null if cast failed, otherwise we change object into
                // list of Tasks and return it
                return jsonArray == null ? null : jsonArray.ToObject<List<Task>>();
            }
            catch (Exception)
            {
                Console.WriteLine("ERROR in getChildren");
                return null;
            }
        }

        private void addMenusToTreeExplorer()
        {
            // Main menu, empty treeView
            treeViewTaskExplorer.ContextMenu =
                treeViewTaskExplorer.Resources["RootMenu"]
                as System.Windows.Controls.ContextMenu;
            // Menu for each node in treeView
            foreach (Object ob in treeViewTaskExplorer.Items)
            {
                TreeViewItem node = ob as TreeViewItem;
                if(node != null)
                {
                    node.ContextMenu = treeViewTaskExplorer.Resources["NodeContextMenu"]
                        as System.Windows.Controls.ContextMenu;
                }
            }
        }

        // Adds a new root task
        private void menuItemAddNewTask1_Click(object sender, RoutedEventArgs e)
        {
            //MessageBox.Show("message", "caption");
            string name = Interaction.InputBox("Choose the name of new task", "Name", "task");
            string description = Interaction.InputBox("Description of the task", "Description", "buy 3 beers");
            Console.WriteLine("name : {0}", name);
            Console.WriteLine("description : {0}", description);
            try
            {
                taskExplorer.addNewTask(description, name,
                     treeViewTaskExplorer);
            }
            catch(Exception)
            {
                MessageBox.Show("Opps! Something went wrong. Try again later!");
            }
        }

        // Adds a new subtask
        private void menuItemAddNewSubtask_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                TreeViewItem parentNode = treeViewTaskExplorer.SelectedItem as TreeViewItem;
                if (parentNode != null)
                {
                    Console.WriteLine("Jestesmy w node: {0}", parentNode.Header.ToString());
                    Task task = parentNode.Tag as Task;
                    if (task != null)
                    {
                        Console.WriteLine("MAMY task! description: {0}", task.description);
                        string name =
                            Interaction.InputBox("Choose the name of new task", "Name", "task");
                        string description =
                            Interaction.InputBox("Description of the task", "Description", "");
                        taskExplorer.addNewSubTask(description, name, task.id,  parentNode);
                    }
                    else
                    {
                        // every node should have Task as a Tag so
                        // it should be like this!
                        // FIXME - only for debugging! should be canceled later
                        MessageBox.Show("ERROR! Node nie ma Task w Tagu!!");
                    }
                }
            }
            catch(Exception)
            {
                MessageBox.Show("Opps! Something went wrong. Try again later!");
            }
        }

        // delete task
        private void menuItemDeleteTask_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                TreeViewItem parentNode = treeViewTaskExplorer.SelectedItem as TreeViewItem;
                if (parentNode != null)
                {
                    Console.WriteLine("Jestesmy w node: {0}", parentNode.Header.ToString());
                    Task task = parentNode.Tag as Task;
                    if (task != null)
                    {
                        Console.WriteLine("MAMY task! description: {0}", task.description);
                        taskExplorer.deleteTask(parentNode);
                        // TODO - mozliwe jeszcze ze przez referencje / inaczej to trzeba usuwac
                    }
                    else
                    {
                        MessageBox.Show("ERROR! Node nie ma Task w Tagu!!");
                    }
                }
            }
            catch (Exception)
            {
                MessageBox.Show("Opps! Something went wrong. Try again later!");
            }
        }

        // change task
        private void menuItemChange_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                TreeViewItem parentNode = treeViewTaskExplorer.SelectedItem as TreeViewItem;
                if (parentNode != null)
                {
                    Console.WriteLine("Jestesmy w node: {0}", parentNode.Header.ToString());
                    Task task = parentNode.Tag as Task;
                    if (task != null)
                    {
                        Console.WriteLine("MAMY task! description: {0}", task.description);
                        string name =
                            Interaction.InputBox("New Name", "Name", "task");
                        string description =
                            Interaction.InputBox("Description of the task", "Description", "");
                        // TODO !! jeszcze 
                        //taskExplorer.addNewSubTask(description, name, task.id,  parentNode);
                    }
                    else
                    {
                        MessageBox.Show("ERROR! Node nie ma Task w Tagu!!");
                    }
                }
            }
            catch(Exception)
            {
                MessageBox.Show("Opps! Something went wrong. Try again later!");
            }
        }
        }

    } // class
} // namespace
