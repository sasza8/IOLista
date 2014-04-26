using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;

using Newtonsoft.Json;

namespace client
{
    /// <summary>
    /// Kazda wiadomosc od i do serwera ma pole 'type'
    /// </summary>
    class Protocol
    {
        private static const int MAX_RECIEVED_MSG_LENGTH = 2048; // in bytes

        //public string type { get; set; }
        public static string TYPE = "type";

        // AUTHENTICATE
        public static string AUTHENTICATE = "authenticate";
        public static string LOGIN_OK = "loginOK";
        public static string LOGIN_FAILED = "loginFailed";
        // REGISTER
        public static string REGISTER = "register";
        public static string REGISTER_OK = "registerOK";
        public static string REGISTER_FAILED = "registerFailed";

        // FUNCTIONS TO GET JSON STRINGS
        public static string jsonAuthenticate(string username, string password)
        {
            return
                @"{
                    'type': '" + AUTHENTICATE + @"',
                    'username': '" + username + @"',
                    'password': '" + password + @"',
                }";
        }

        public static string jsonRegister(string username, string firstName,
            string lastName, string email, string password)
        {
            return
                @"{
                    'type': '" + REGISTER + @"'
                    'username': '" + username + @"',
                    'firstname': '" + firstName + @"',
                    'lastname': '" + lastName + @"',
                    'email': '" + email + @"',
                    'password': '" + password + @"',
                }";
        }

        // SENDIND / RECIEVING / JSON
        public static void sendToServer(NetworkStream stream, String msg)
        {
            Byte[] data = System.Text.Encoding.ASCII.GetBytes(msg);
            stream.Write(data, 0, data.Length);
        }

        public static String recieveFromServer(NetworkStream stream)
        {
            byte[] data = new byte[MAX_RECIEVED_MSG_LENGTH];
            // Read the first batch of the TcpServer response bytes.
            Int32 bytes = stream.Read(data, 0, data.Length);

            return System.Text.Encoding.ASCII.GetString(data, 0, bytes);
        }

        public static Dictionary<String, String> jsonToDictionary(String jsn)
        {
            return JsonConvert.DeserializeObject<Dictionary<String, String>>(jsn);
        }


    } // class
}
