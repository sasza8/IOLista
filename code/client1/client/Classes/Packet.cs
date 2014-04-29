using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace client
{
    class Packet
    {
        public string type { get; set; }
        public Dictionary<string, object> parameters { get; set; }

        public Packet()
        {
            parameters = new Dictionary<string,object>();
        }
    }
}
