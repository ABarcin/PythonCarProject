using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace PythonCarProject.UI.Models
{
    public class Car
    {
        public string Brand { get; set; }
        public string Color { get; set; }
        public string Year { get; set; }
        public string Title { get; set; }
        public string Transmission { get; set; }
        public string Price { get; set; }
        public string ImagePath { get; set; }
    }
}
