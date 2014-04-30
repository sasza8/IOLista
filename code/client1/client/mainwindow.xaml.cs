using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

// do testow
using Newtonsoft.Json;
using Microsoft.VisualBasic;

namespace client
{

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private const int PORT = 16661;
        private const string HOSTNAME = "localhost";

        private TcpClient client;

        public MainWindow()
        {
            InitializeComponent();
        }

        // Nawiazujemy polaczenie z serverem. Gdy cos sie nie uda - wychodzimy
        private void Grid_Loaded(object sender, RoutedEventArgs e)
        {         
            //try
            //{
            //    // ArgumentNullException - hostname null
            //    // ArgumentOutOfRangeException - zly port
            //    // SocketException
            //    client = new TcpClient();
            //    client.Connect(HOSTNAME, PORT);
            //}
            //catch (Exception ex)
            //{
            //    // FIXME
            //    // tutaj ewentualne wyjscie z programu/ wlaczenie trybu offline
            //    Console.WriteLine("SocketException / WrongPort : {0}", ex);
            //    MessageBox.Show("Nie udalo sie polaczyc z serwerem :(");
            //    MessageBox.Show("KOD BLEDU: " + ex.ToString());
            //}
        }

        private void btnLogin_Click(object sender, RoutedEventArgs e)
        {
            string username = txtBoxLogin.Text;
            string password = passwordBox.Password;
            Console.Write("login: {0}", username);
            Console.Write("pasword: {0}", password);
            try
            {
                NetworkStream stream = client.GetStream();
                PacketCTS packet =
                    Protocol.getPacketAuthenticate(username, password);

                Protocol.sendToServer(stream, packet);
                PacketSTC response = Protocol.recieveFromServer(stream);
                checkAuthentication(username, response);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error in LOGIN : {0}", ex);
            }
        }

        private void btnRegister_Click(object sender, RoutedEventArgs e)
        {
            //Register window = new Register(client);
            //window.Show();

            // TESTTT
            PacketSTC packetTest = new PacketSTC();
            packetTest.type = Protocol.LOGIN_OK;
            packetTest.parameters.Add("authToken", "mojTokenik");
            checkAuthentication("Pablo", packetTest);
        }


        // **                 PRIVATE FUNCTIONS             **/
        // ***************************************************/

        private void checkAuthentication(string username, PacketSTC serverResponse)
        {
            if (serverResponse.type.Equals(Protocol.LOGIN_OK))
            {
                // Server sends us authToken as a attribute of params dictionary!
                LoggedHome window = new LoggedHome(username,
                    (string) serverResponse.parameters["authToken"], client);
                window.Show();
                this.Close();
            }              
            else // TUTAJ ewentualne sprawdzanie czy LOGIN_FAIL i nowy else - zly pakiet :(
            {
                MessageBox.Show("Blad w logowaniu");
            }               
        }

        private void btnTest_Click(object sender, RoutedEventArgs e)
        {
//            string json = @"{
//  'description': 'opis bla bla bla',
//  'releaseDate': '1995-4-7T00:00:00',
//    'lastModificationDate': '1995-4-7T00:00:00',
//    'done' : 'False',
//  'subTasks': [
//{  'description': 'OPIS WEWNATRZ',
//  'releaseDate': '1995-4-7T00:00:00',
//    'lastModificationDate': '1995-4-7T00:00:00',
//    'done' : 'False',
//  'subTasks': []},
//  ]
//}";
//            Task task =
//                JsonConvert.DeserializeObject<Task>(json);
//            Console.WriteLine("{0}", task.description);
//                Console.WriteLine("{0}", task.createOn);
//                Console.WriteLine("{0}", task.lastChange);
//                Console.WriteLine("{0}", task.done);
//                Console.WriteLine("{0}", task.subtasks[0].description);

//                Task t = new Task();
//                t.description = "test desc";
//                t.lastChange = "jakasData";
//                t.createOn = "innaData";
//                t.done = true;
//                    //t.subtasks = new Task[10];
//                t.subtasks.Add(task);
//                string jsonString = JsonConvert.SerializeObject(t);
//                Console.WriteLine("{0}", jsonString);
//                string json = @"{
//'type' : 'loginOK',
//'parameters' : {
//    'subtasks' : [ { 'bla' : 'bla1',},
//    {'bla' : 'bla2',}, ],
//    'gruszka' : 'grucha',
//    'jablko' : 'japco',
//},
//}";
//                Dictionary<string, string> d = JsonConvert.DeserializeObject<Dictionary<string, string>>(json);
//               Console.WriteLine("type: {0}", d["type"]);
//                Console.WriteLine("params[0]: {0}", d["parameters"]);
        }

        private void btnPolaczZSerwerem_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // ArgumentNullException - hostname null
                // ArgumentOutOfRangeException - zly port
                // SocketException
                string hostname =
                    Interaction.InputBox("HOSTNAME", "HOSTNAME", "localhost/127.0.0.1");
                string porcik =
                    Interaction.InputBox("PORT", "PORT", "16661");
                client = new TcpClient();
                Console.WriteLine("HOSTNAME: {0}", hostname);
                Console.WriteLine("PORT: {0}", Convert.ToInt32(porcik));
                client.Connect(hostname, Convert.ToInt32(porcik));
            }
            catch (Exception ex)
            {
                // FIXME
                // tutaj ewentualne wyjscie z programu/ wlaczenie trybu offline
                Console.WriteLine("SocketException / WrongPort : {0}", ex);
                MessageBox.Show("Nie udalo sie polaczyc z serwerem :(");
                MessageBox.Show("KOD BLEDU: " + ex.ToString());
            }
        }

    } // window class
} // namespace
