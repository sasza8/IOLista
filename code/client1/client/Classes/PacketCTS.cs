using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace client
{
    class PacketCTS
    {
        public string type { get; set; }
        public string authToken { get; set; }
        public Dictionary<string, object> parameters { get; set; }

        public PacketCTS()
        {
            parameters = new Dictionary<string,object>();
        }
    }
}
