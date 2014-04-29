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
            taskExplorer = new TaskExplorer();
        }

        private void Grid_Loaded(object sender, RoutedEventArgs e)
        {
            // FIXME
            // gdy okienko sie wczyta to wysyłamy rządanie o
//            // pierwsza warstwe taskow!
//            listViewTasks.Items.Add(new Task
//            {
//                id = 1,
//                createOn = "dzisiaj",
//                lastChange = "mnute temu",
//                done = false,
//                parent = 1,
//                description = @"
//                taki tam opis projektu, kpic cos"
//            });
//            listViewTasks.Items.Add(new Task
//            {
//                id = 2,
//                createOn = "wczoraj",
//                lastChange = "teraz",
//                done = true,
//                parent = 2,
//                description = @"
//                BLA BLA BLA BLA ploooo"
//            });
            try
            {
                NetworkStream stream = client.GetStream();
                string msg = Protocol.jsonSubtasks(-1);
                Protocol.sendToServer(stream, msg);
                string response = Protocol.recieveFromServer(stream);
                uberTask = JsonConvert.DeserializeObject<UberTask>(response);
                // TODO
                // mamy juz uberTask, teraz trzeba go jakos wyswietlic
            }
            catch
            {
                // TODO
                Console.WriteLine("BLAD w LOADED");
            }
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
                taskExplorer.addNewTask(t, treeViewTaskExplorer);
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
        }

        // ***************** PRIVATE FUNCTIONS ************ //
        // ************************************************ //

        private void addMenusToTreeExplorer()
        {
            // TODO
            foreach( TreeViewItem RootNode in treeViewTaskExplorer.Items)
            {
                //RootNode.Parent;
            }
        }

    } // class
} // namespace
