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
            try
            {
                // ArgumentNullException - hostname null
                // ArgumentOutOfRangeException - zly port
                // SocketException
                client = new TcpClient(HOSTNAME, PORT);
            }
            catch (Exception ex)
            {
                // FIXME
                // tutaj ewentualne wyjscie z programu/ wlaczenie trybu offline
                Console.WriteLine("SocketException / WrongPort : {0}", ex);
            }
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
                string json =
                    Protocol.jsonAuthenticate(username, password);

                Protocol.sendToServer(stream, json);

                String response = Protocol.recieveFromServer(stream);

                checkAuthentication(username, response);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error in LOGIN : {0}", ex);
            }
        }

        private void btnRegister_Click(object sender, RoutedEventArgs e)
        {
            Register window = new Register(client);
            window.Show();
//              // TESTTT
//            string jsnTest = @"{
//                'type': '" + ServerResponse.LOGIN_OK + @"',
//                'token': 'blablablaTOKEN',
//            }";

//            Dictionary<String, String> d =
//                JsonConvert.DeserializeObject<Dictionary<String, String>>(jsnTest);

//            Console.WriteLine("Type: {0}", d[ServerResponse.TYPE]);
//            checkAuthentication("Pablo", jsnTest);
        }


        // **                 PRIVATE FUNCTIONS             **/
        // ***************************************************/

        private void checkAuthentication(String username, String serverResponse)
        {
            // konwertujemy JSONa na klase Slownik
            Dictionary<String, String> dictionary =
                Protocol.jsonToDictionary(serverResponse);

            if (dictionary[Protocol.TYPE].Equals(Protocol.LOGIN_OK))
            {
                LoggedHome window = new LoggedHome(username, dictionary["token"]);
                window.Show();
                this.Close();
            }              
            else // TUTAJ ewentualne sprawdzanie czy LOGIN_FAIL i nowy else - zly pakiet :(
            {
                MessageBox.Show("Blad w logowaniu");
            }               
        }

    } // window class
} // namespace
