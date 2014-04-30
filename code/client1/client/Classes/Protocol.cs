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
        // FIXME
        // CZY TA DLUGOSC NIE ZA MALA! JAK TO ZROBIC INACZEJ !?
        // uzywane w recieveFromServer(NetworkStream stream)
        private const int MAX_RECIEVED_MSG_LENGTH = 4096; // in bytes

        // AUTHENTICATE
        public static string AUTHENTICATE = "authenticate";
        public static string LOGIN_OK = "loginOK";
        public static string LOGIN_FAILED = "loginFailed";
        // REGISTER
        public static string REGISTER = "register";
        public static string REGISTER_OK = "registerOK";
        public static string REGISTER_FAILED = "registerFailed";
        // TASKS - GET
        public static string GET_TASKS = "getTasks";
        public static string TASKS = "tasks";
        public static string AUTHENTITACION_REQUIRED = "authenticationRequired";
        // TASKS - ADD
        public static string ADD_TASK = "addTask";
        public static string ADD_TASK_OK = "addTaskOK";
        public static string ADD_TASK_FAILED = "addTaskFailed";
        // TASKS - DELETE
        public static string DELETE_TASK = "deleteTask";
        public static string DELETE_TASK_OK = "deleteTaskOK";
        public static string DELETE_TASK_FAILED = "deleteTaskFailed";
        public static string OPERATION_NOT_ALLOWED = "operationNotAllowed";
                // AUTHENTITACION_REQUIRED
        // TASKS - UPDATE
        public static string UPDATE_TASK = "updateTask";
        public static string UPDATE_TASK_OK = "updateTaskOK";
        public static string UPDATE_TASK_FAILED = "updateTaskFailed";
                // AUTHENTITACION_REQUIRED
                // OPERATION_NOT_ALLOWED
       

        // FUNCTIONS TO GET PACKETS
        public static PacketCTS getPacketAuthenticate(string username, string password)
        {
            PacketCTS p = new PacketCTS();
            p.type = AUTHENTICATE;
            p.parameters.Add("username", username);
            p.parameters.Add("password", password);

            return p;
        }

        public static PacketCTS getPacketRegister(string username,
            string email, string password)
        {
            PacketCTS p = new PacketCTS();
            p.type = REGISTER;
            p.parameters.Add("username", username);
            p.parameters.Add("password", password);
            p.parameters.Add("email", email);

            return p;
        }
        
        /// <summary>
        /// Gets all children of parent node , if parent == -1 => gets root nodes
        /// </summary>
        /// <param name="parent"> parents id. -1 to get root tasks</param>
        /// <returns></returns>
        public static PacketCTS getPacketSubtasks(int parent, string authToken)
        {
            PacketCTS p = new PacketCTS();
            p.type = GET_TASKS;
            p.authToken = authToken;
            if( parent >= 0 )
                p.parameters.Add("parent", parent);        

            return p;
        }

        /// <summary>
        /// adds child to parent node, if parent == -1 then adds root node
        /// </summary>
        /// <param name="parent"> parents id, -1 when root</param>
        /// <param name="description"></param>
        /// <param name="authToken"></param>
        /// <returns></returns>
        public static PacketCTS getPacketAddTask(int parent, string description,
            string authToken)
        {
            PacketCTS p = new PacketCTS();
            p.type = ADD_TASK;
            p.authToken = authToken;
            p.parameters.Add("description", description);
            if(parent >= 0 )
                p.parameters.Add("parent", parent);

            return p;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="id"> id of task we want to delete </param>
        /// <param name="authToken"></param>
        /// <returns></returns>
        public static PacketCTS getPacketDeleteTask(int id, string authToken)
        {
            PacketCTS p = new PacketCTS();
            p.type = DELETE_TASK;
            p.authToken = authToken;
            p.parameters.Add("id", id);

            return p;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="id"> id of task to delete</param>
        /// <param name="parentId"></param>
        /// <param name="name"></param>
        /// <param name="description"></param>
        /// <returns></returns>
        public static PacketCTS getPacketUpdateTask(int id, int parentId,
            string name, string description, string authToken)
        {
            PacketCTS p = new PacketCTS();
            p.type = UPDATE_TASK;
            p.authToken = authToken;
            p.parameters.Add("id", id);
            p.parameters.Add("parentId", parentId);
            p.parameters.Add("name", name);
            p.parameters.Add("description", description);

            return p;
        }


        // SENDIND / RECIEVING
        public static void sendToServer(NetworkStream stream, PacketCTS packet)
        {
            string msg = JsonConvert.SerializeObject(packet);
            Byte[] data = System.Text.Encoding.ASCII.GetBytes(msg);
            stream.Write(data, 0, data.Length);
        }
        
        // returns json from serwer
        public static PacketSTC recieveFromServer(NetworkStream stream)
        {
            byte[] data = new byte[MAX_RECIEVED_MSG_LENGTH];
            // Read the first batch of the TcpServer response bytes.
            Int32 bytes = stream.Read(data, 0, data.Length);
            string json = System.Text.Encoding.ASCII.GetString(data, 0, bytes);

            return JsonConvert.DeserializeObject<PacketSTC>(json);
        }

    } // class
}
