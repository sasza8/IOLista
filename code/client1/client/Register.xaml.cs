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

namespace client
{
    /// <summary>
    /// Interaction logic for Register.xaml
    /// </summary>
    public partial class Register : Window
    {
        private TcpClient client;

        public Register(TcpClient _client)
        {
            InitializeComponent();
            client = _client;
        }

        private void btnCancel_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }

        private void btnSubmit_Click(object sender, RoutedEventArgs e)
        {
            //TODO
            // TUTAJ prawdopodobnie validacja formy i wyswietlenie uzytkownikowi
            // co wpisal zle
            // validateForm()
            string username, email, password;
            username = txtBoxUsername.Text;
            email = txtBoxEmail.Text;
            password = passwordBox1.Password;
            try 
            {
                NetworkStream stream = client.GetStream();
                PacketCTS packet = Protocol.getPacketRegister(username, email, password);           

                Protocol.sendToServer(stream, packet);
                PacketSTC response = Protocol.recieveFromServer(stream);
                checkRegistration(response);
            }
            catch (Exception ex)
            {
                // TODO
                Console.WriteLine("Register exception : {0}", ex);
                MessageBox.Show("Blad z polaczeniem z serwerem, internety zle dzialaja");
            }
        }


        // **                  PRIVATE FUNCTIONS            **//
        // ***************************************************//

        // true gdy wszystko OK
        private bool validateForm()
        {
            // TODO
            return true; 
        }

        private void checkRegistration(PacketSTC serverResponse)
        {

            if(serverResponse.type.Equals(Protocol.REGISTER_OK))
            {
                Console.WriteLine("Registation OK");
                MessageBox.Show("All went fine!");
                this.Close();
            }
            else
            {
                MessageBox.Show("Oopps, error");
                Console.WriteLine("Registation FAILED");
            }
        }

    } // class
} // namespace
