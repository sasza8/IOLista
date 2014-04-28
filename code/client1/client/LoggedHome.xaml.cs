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

        UberTask uberTask;

        public LoggedHome(string _username, string _token, TcpClient _client)
        {
            InitializeComponent();
            username = _username;
            token = _token;
            client = _client;
        }

        private void Grid_Loaded(object sender, RoutedEventArgs e)
        {
            // FIXME
            // gdy okienko sie wczyta to wysyłamy rządanie o
            // pierwsza warstwe taskow!
            listViewTasks.Items.Add(new Task
            {
                id = 1,
                createOn = "dzisiaj",
                lastChange = "mnute temu",
                done = false,
                parent = 1,
                description = @"
                taki tam opis projektu, kpic cos"
            });
            listViewTasks.Items.Add(new Task
            {
                id = 2,
                createOn = "wczoraj",
                lastChange = "teraz",
                done = true,
                parent = 2,
                description = @"
                BLA BLA BLA BLA ploooo"
            });
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



    } // class
} // namespace
