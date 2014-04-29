using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace client
{
    class Task
    {
        public int id { get; set; } 
        public int parent { get; set; } // -1 when root node

        public string name { get; set; }
        public string description { get; set; }
        public string createOn { get; set; }
        public string lastChange { get; set; }
        public bool done { get; set; } // bool

        //// czy to potrzebne???? czy w treeView juz tego nei mamy zalatwionego?
        //public List<Task> subtasks { get; set; }

        //public Task()
        //{
        //    subtasks = new List<Task>();
        //}
    }
}
