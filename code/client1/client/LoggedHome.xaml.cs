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

        private UberTask uberTask;
        private TaskExplorer taskExplorer;

        public LoggedHome(string _username, string _token, TcpClient _client)
        {
            InitializeComponent();
            username = _username;
            token = _token;
            client = _client;
            taskExplorer = new TaskExplorer(_client);
        }

        private void Grid_Loaded(object sender, RoutedEventArgs e)
        {
            UberTask rootTasks = getChildren(-1);
            if(rootTasks != null)
               initTreeView(rootTasks);

            addMenusToTreeExplorer();
        }

        private void btnTest_Click(object sender, RoutedEventArgs e)
        {
            string response =
                @"{
                    'subtasks' :
[
{
               'id' : '1',
               'createOn': 'zisiaj',
               'lastChange': 'mnute temu',
               'done': 'False',
               'parent': '1',
               'description':  'opis',
               'name' : 'posprzataj pokoj',
               'subtasks' : [], 
},
{
               'id' : '2',
               'createOn': 'wczoraj',
               'lastChange': 'mnute temu',
               'done': 'True',
               'parent': '1',
               'description':  'blalblalbla opis',
               'name' : 'name2',
               'subtasks' : [], 
},
{
               'id' : '3',
               'createOn': 'zisiaj',
               'lastChange': 'mnute temu',
               'done': 'false',
               'parent': '1',
               'description':  'opis',
               'name' : 'name3',
               'subtasks' : [], 
},
],
}";
            uberTask = JsonConvert.DeserializeObject<UberTask>(response);
            foreach(Task t in uberTask.subtasks)
            {
                //taskExplorer.addNewTask(t, treeViewTaskExplorer);
            }
            foreach (Object ob in treeViewTaskExplorer.Items)
            {
                TreeViewItem node = ob as TreeViewItem;
                if(node != null)
                {
                    node.ContextMenu = treeViewTaskExplorer.Resources["NodeContextMenu"]
                        as System.Windows.Controls.ContextMenu;
                }
            }
            treeViewTaskExplorer.ContextMenu =
                treeViewTaskExplorer.Resources["RootMenu"] 
                as System.Windows.Controls.ContextMenu;
        }

        // ***************** PRIVATE FUNCTIONS ************ //
        // ************************************************ //

        /// <summary>
        /// Initializes the treeView! adds all nodes
        /// </summary>
        /// <param name="uberTask">root nodes!</param>
        private void initTreeView(UberTask uberTask)
        {
            foreach(Task rootTask in uberTask.subtasks)
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
            UberTask children = getChildren(parentId);
            if(children != null)
            {
                foreach(Task subtask in children.subtasks)
                {
                    TreeViewItem subtaskNode = 
                        taskExplorer.addNewSubtaskToTreeView(subtask, parentNode);
                    // resursion!
                    addSubtasks(subtaskNode, subtask.id);
                }
            }
        }

        /// <summary>
        /// Returns chidlren of a parent as a UberTask or null if sth wen wrong
        /// </summary>
        /// <param name="parentId"> parents id, use -1 to get root nodes </param>
        /// <returns></returns>
        private UberTask getChildren(int parentId)
        {
            try
            {
                NetworkStream stream = client.GetStream();
                string msg = Protocol.jsonSubtasks(parentId, token);
                Protocol.sendToServer(stream, msg);
                string response = Protocol.recieveFromServer(stream);
                return JsonConvert.DeserializeObject<UberTask>(response);
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
                    token, treeViewTaskExplorer);
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
                    Console.WriteLine("Jestesmy w node");
                    Task task = parentNode.Tag as Task;
                    if (task != null)
                    {
                        Console.WriteLine("MAMY task! description: {0}", task.description);
                        string name =
                            Interaction.InputBox("Choose the name of new task", "Name", "task");
                        string description =
                            Interaction.InputBox("Description of the task", "Description", "");
                        taskExplorer.addNewSubTask(description, name, task.id, token, parentNode);
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

    } // class
} // namespace
