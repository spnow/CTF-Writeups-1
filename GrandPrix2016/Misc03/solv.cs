using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Security.Cryptography;
using System.IO;

namespace Misc
{
    class Program
    {
        static void Main(string[] args)
        {
                ss = new Random(456360765);
                string password = genRandomString(0x28);
                byte[] value = SHA1.Create().ComputeHash(Encoding.UTF8.GetBytes(genRandomString(0x1e)));
                string hash = BitConverter.ToString(value).Replace("-", string.Empty);
                Console.WriteLine("Password: " + password);
                Console.WriteLine("Hash: "+hash);
                Console.WriteLine("Flag: "+dec(@"C:\Users\BM\Desktop\IDM-silent\flag.1F75BF558F2BD3642A3D88B7B870FA52D5B90B3B", password));
                //Flag: 7h4nks_f0r_y0ur_3ff0rt
        }

        public static string dec(string file_name, string password)
        {
            byte[] file_content = File.ReadAllBytes(file_name);
            byte[] key = Encoding.UTF8.GetBytes(password);
            key = SHA256.Create().ComputeHash(key);
            Console.WriteLine("key: "+ByteArrayToString(key));
            string bytes = Encoding.UTF8.GetString(decrypt(file_content, key));
            return bytes;
        }
        public static string ByteArrayToString(byte[] ba)
        {
            string hex = BitConverter.ToString(ba);
            return hex.Replace("-", "");
        }
        public static byte[] decrypt(byte[] data, byte[] drive_byte)
        {
            byte[] result = null;
            using (MemoryStream memoryStream = new MemoryStream())
            {
                using (RijndaelManaged rijndaelManaged = new RijndaelManaged())
                {
                    rijndaelManaged.KeySize = 256;
                    rijndaelManaged.BlockSize = 128;
                    Rfc2898DeriveBytes rfc2898DeriveBytes = new Rfc2898DeriveBytes(drive_byte, drive_byte, 0x3e8);
                    rijndaelManaged.Key = rfc2898DeriveBytes.GetBytes(256/8);
                    rijndaelManaged.IV = rfc2898DeriveBytes.GetBytes(128/8);
              
                    rijndaelManaged.Mode = (CipherMode)0x01;
                    using (CryptoStream cryptoStream = new CryptoStream(memoryStream, rijndaelManaged.CreateDecryptor(), (CryptoStreamMode)0x01))
                    {
                        cryptoStream.Write(data, 0, data.Length);
                        cryptoStream.Close();
                    }
                    result = memoryStream.ToArray();
                }
            }
            return result;
        }
        
        private static Func<string, char> bb;
        public static string genRandomString(int ax)
        {
            IEnumerable<string> expr_12 = Enumerable.Repeat<string>("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890qwertyuiopasdfghjklzxcvbnm0123456789", ax);
            if (bb == null)
            {
                bb = new Func<string, char>(cc);
            }
            string a = new string(expr_12.Select(bb).ToArray<char>());
   
            return a;
        }
        private static Random ss;
        private static char cc(string input)
        {
            return input[ss.Next(input.Length)];
        }
        
    }
}
