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
            String username, firstName, lastName, email, password;
            username = txtBoxUsername.Text;
            firstName = txtBoxFirstName.Text;
            lastName = txtBoxLastName.Text;
            email = txtBoxEmail.Text;
            password = passwordBox1.Password;
            try 
            {
                NetworkStream stream = client.GetStream();
                String jsn = Protocol.jsonRegister(username, firstName,
                     lastName, email, password);           

                Protocol.sendToServer(stream, jsn);
                String response = Protocol.recieveFromServer(stream);

                checkRegistration(response);
            }
            catch (Exception ex)
            {
                // TODO
                Console.WriteLine("Register exception : {0}", ex);
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

        private void checkRegistration(String serverResponse)
        {
            Dictionary<String, String> dict =
                Protocol.jsonToDictionary(serverResponse);
            String type = dict[Protocol.TYPE];
            if(type.Equals(Protocol.REGISTER_OK))
            {
                // TODO
                Console.WriteLine("Registation OK");
            }
            else if(type.Equals(Protocol.REGISTER_FAILED))
            {
                // TODO
                Console.WriteLine("Registation FAILED");
            }
            else // zly pakiet!
            {
                // TODO
                Console.WriteLine("Registation : WRONG PACKET");
            }
        }

    } // class
} // namespace
