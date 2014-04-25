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
                string json =
                    ServerPackets.Authenticate.json(username, password);
                // Translate the passed message into ASCII and store it as a Byte array.
                Byte[] data = System.Text.Encoding.ASCII.GetBytes(json);   

                //InvalidOperationException - client niepolaczony
                //ObjectDisposedException - client zostal zamkniety
                NetworkStream stream = client.GetStream();

                stream.Write(data, 0, data.Length);

                //teraz odpowiedz serwera
                data = new byte[1024];
                String response = String.Empty;

                // Read the first batch of the TcpServer response bytes.
                Int32 bytes = stream.Read(data, 0, data.Length);
                response = System.Text.Encoding.ASCII.GetString(data, 0, bytes);
                Console.WriteLine("Received: {0}", response);

                // TODO - nowe okno przy pomyslnym zalogowaniu + przekazanie
                // nazwy uzytkownika itp
                if (response.Equals(ServerPackets.ServerResponse.LOGIN_OK))
                    MessageBox.Show("Zalogowano pomyslnie");
                else
                    MessageBox.Show("BLad w logowaniu");

            }
            catch (Exception ex)
            {
                Console.WriteLine("Error in LOGIN : {0}", ex);
            }
        }

    } // window class
} // namespace
