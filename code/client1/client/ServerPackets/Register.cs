using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace client.ServerPackets
{
    class Register
    {
        public string type { get; set; }
        public string username { get; set; }
        public string password { get; set; }
        public string firstname { get; set; }
        public string lastname { get; set; }
        public string email { get; set; }

    }
}
