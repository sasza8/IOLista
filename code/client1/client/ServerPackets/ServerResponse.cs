using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace client.ServerPackets
{
    class ServerResponse
    {
        public string type { get; set; }

        // LOGOWANIE
        public static string LOGIN_OK = "loginOk";
        public static string LOGIN_FAILED = "loginFailed";

        // REJESTROWANIE
        public static string REGISTER_OK = "registerOk";
        public static string REGISTER_FAILED = "registerFailed";
    }
}
