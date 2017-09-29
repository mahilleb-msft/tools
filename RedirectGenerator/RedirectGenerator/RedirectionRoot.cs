using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RedirectGenerator
{
    public class RedirectionRoot
    {
        public RedirectionRoot()
        {
            RedirectionObjects = new List<RedirectionObject>();
        }
        [JsonProperty(PropertyName = "redirections")]
        public List<RedirectionObject> RedirectionObjects { get; set; }
    }
}
