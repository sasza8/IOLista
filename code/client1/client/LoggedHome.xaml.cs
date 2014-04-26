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

namespace client
{
    /// <summary>
    /// Interaction logic for LoggedHome.xaml
    /// </summary>
    public partial class LoggedHome : Window
    {
        private String username;
        private String token;

        public LoggedHome(String _username, String _token)
        {
            InitializeComponent();
            username = _username;
            token = _token;
        }

    } // class
} // namespace
