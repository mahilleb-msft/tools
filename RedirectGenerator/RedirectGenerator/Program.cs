using CommandLine;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using YamlDotNet.RepresentationModel;

namespace RedirectGenerator
{
    class Program
    {
        static void Main(string[] args)
        {
            ParserResult<CommandLineOptions> options = Parser.Default.ParseArguments<CommandLineOptions>(args);

            if (options != null)
            {
                options.WithParsed(t => ProcessData(t));
            }

            Console.Read();
        }

        static void ProcessData(CommandLineOptions options)
        {
            if (!string.IsNullOrWhiteSpace(options.ContentPath) && !string.IsNullOrWhiteSpace(options.BaseUrl)
                && !string.IsNullOrWhiteSpace(options.TargetFolder) && !string.IsNullOrWhiteSpace(options.RepoRoot))
            {
                RedirectionRoot root = new RedirectionRoot();


                if (options.MetaType == "ASPNET_LEGACY")
                {
                    var filesNeedingToBeRedirected = Directory.GetFiles(options.ContentPath);

                    if (filesNeedingToBeRedirected != null)
                    {
                        Parallel.ForEach(filesNeedingToBeRedirected, async (file) =>
                        {
                            if (!Path.GetFileName(file).StartsWith(".") && !Path.GetFileName(file).StartsWith("toc.yml"))
                            {
                                var targetUrl = "https://docs.microsoft.com" + options.BaseUrl + "/" + Path.GetFileNameWithoutExtension(file);

                                HttpWebRequest request = (HttpWebRequest)WebRequest.Create(targetUrl);
                                request.Method = "HEAD";
                                request.Timeout = int.MaxValue;
                                request.AutomaticDecompression = DecompressionMethods.Deflate | DecompressionMethods.GZip;

                                try
                                {
                                    var response = (HttpWebResponse)request.GetResponse();

                                    if (options.DeleteFiles)
                                    {
                                        File.Delete(file);
                                    }
                                    root.RedirectionObjects.Add(new RedirectionObject()
                                    {
                                        SourcePath = file.Replace(options.RepoRoot, "").Replace(@"\", @"/").Remove(0, 1),
                                        RedirectUrl = options.BaseUrl + "/" + Path.GetFileNameWithoutExtension(file),
                                        RedirectDocumentId = true
                                    });

                                    Console.WriteLine("Created redirect for " + targetUrl);
                                }
                                catch (Exception ex)
                                {
                                    Console.WriteLine("Failed redirect for " + targetUrl);
                                }
                            }
                        });
                    }
                }
                else if (options.MetaType == "NODEJS")
                {
                    var pathToToc = Path.Combine(options.ContentPath, "toc.yml");
                    var tocInput = new StringReader(File.ReadAllText(pathToToc));

                    var tocYaml = new YamlStream();
                    tocYaml.Load(tocInput);

                    var mapping = (YamlSequenceNode)tocYaml.Documents[0].RootNode;
                    foreach (var entry in mapping.Children)
                    {
                        // TODO: Here we create package redirections. Thos are currently custom-written,
                        // so we just need a list.
                        var serviceName = ((YamlMappingNode)entry).Children["uid"].ToString();

                        root.RedirectionObjects.Add(new RedirectionObject()
                        {
                            SourcePath = "docs-ref-autogen/overview/azure/INSERT_SERVICE_NAME/" + serviceName + ".yml",
                            RedirectUrl = "/javascript/api/overview/azure/INSER_SERVICE_NAME_HERE/" + serviceName,
                            RedirectDocumentId = true
                        });

                        YamlSequenceNode items = ((YamlMappingNode)entry).Children["items"] as YamlSequenceNode;

                        foreach (var child in items.Children)
                        {
                            var redirectionTarget = ((YamlMappingNode)child).Children["uid"].ToString().Replace('.', '/');

                            var targetUrl = "https://docs.microsoft.com" + options.BaseUrl + "/" + redirectionTarget;

                            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(targetUrl);
                            request.Method = "HEAD";
                            request.Timeout = int.MaxValue;
                            request.AutomaticDecompression = DecompressionMethods.Deflate | DecompressionMethods.GZip;

                            try
                            {
                                var response = (HttpWebResponse)request.GetResponse();

                                Console.WriteLine("Existing cotnent will be redirected: " + redirectionTarget);

                                root.RedirectionObjects.Add(new RedirectionObject()
                                {
                                    SourcePath = "docs-ref-autogen/" + redirectionTarget + ".yml",
                                    RedirectUrl = "/javascript/api/" + redirectionTarget,
                                    RedirectDocumentId = true
                                });

                                Console.WriteLine("Created redirect for " + targetUrl);
                            }
                            catch (Exception ex)
                            {
                                Console.WriteLine("Failed redirect for " + targetUrl);
                            }
                        }
                    }
                }

                var jsonString = JsonConvert.SerializeObject(root);

                File.WriteAllText(Path.Combine(options.TargetFolder, ".openpublishing.redirection.json"), jsonString);
                Console.WriteLine("Redirection file generation complete.");
            }
        }
    }
}
