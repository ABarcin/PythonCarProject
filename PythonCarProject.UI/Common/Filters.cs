using Microsoft.AspNetCore.Mvc.Rendering;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace PythonCarProject.UI.Common
{
    public static class Filters
    {
        public static List<SelectListItem> Brands { get; set; }
        public static List<SelectListItem> Colors { get; set; }
        public static List<SelectListItem> Years { get; set; }
        public static List<SelectListItem> Trans { get; set; }
    }
}
