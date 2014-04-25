using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace client.ServerPackets
{
    class Authenticate
    {
        // type of msg. See protocol
        private const string authenticate = "authenticate";

        public string type { get; set; }
        public string username { get; set; }
        public string password { get; set; }

        public static string json(string username, string password)
        {
            return
                @"{
                    'type': '" + authenticate + @"'
                    'username': '" + username + @"'
                    'password': '" + password + @"'
                }";
        }
    }
}
