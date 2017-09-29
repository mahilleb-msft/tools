using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace RedirectGenerator
{
    public class RedirectionObject
    {
        [JsonProperty(PropertyName = "source_path")]
        public string SourcePath { get; set; }
        [JsonProperty(PropertyName = "redirect_url")]
        public string RedirectUrl { get; set; }
        [JsonProperty(PropertyName = "redirect_document_id")]
        public bool RedirectDocumentId { get; set; }
    }
}
