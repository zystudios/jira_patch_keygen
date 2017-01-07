import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.StringWriter;
import java.io.UnsupportedEncodingException;
import java.io.IOException;
import java.security.InvalidKeyException;
import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.PublicKey;
import java.security.Signature;
import java.security.SignatureException;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.X509EncodedKeySpec;
import java.util.Properties;
import java.util.zip.Inflater;
import java.util.zip.InflaterInputStream;
import org.apache.commons.codec.binary.Base64;
import org.apache.commons.io.IOUtils;

public class Decoder
{

  public static final int VERSION_NUMBER_1 = 1;
  public static final int VERSION_NUMBER_2 = 2;
  public static final int VERSION_LENGTH = 3;
  public static final int ENCODED_LICENSE_LENGTH_BASE = 31;
  public static final byte[] LICENSE_PREFIX = { 13, 14, 12, 10, 15 };
  public static final char SEPARATOR = 'X';
  private static final PublicKey PUBLIC_KEY;
  private static final int ENCODED_LICENSE_LINE_LENGTH = 76;

  public boolean canDecode(String licenseString)
  {
    licenseString = removeWhiteSpaces(licenseString);

    int pos = licenseString.lastIndexOf('X');
    if ((pos == -1) || (pos + 3 >= licenseString.length()))
    {
      return false;
    }

    try
    {
      int version = Integer.parseInt(licenseString.substring(pos + 1, pos + 3));
      if ((version != 1) && (version != 2))
      {
        return false;
      }

      String lengthStr = licenseString.substring(pos + 3);
      int encodedLicenseLength = Integer.valueOf(lengthStr, 31).intValue();
      if (pos != encodedLicenseLength)
      {
        return false;
      }

      return true;
    }
    catch (NumberFormatException e) {
    }
    return false;
  }

  public void doDecode(String licenseString)
     throws Exception
  {
    String encodedLicenseTextAndHash = getLicenseContent(removeWhiteSpaces(licenseString));
    byte[] zippedLicenseBytes = checkAndGetLicenseText(encodedLicenseTextAndHash);
    saveBytes("bytes.txt", zippedLicenseBytes);
    Reader licenseText = unzipText(zippedLicenseBytes);

    try {
        StringWriter writer = new StringWriter();
        //IOUtils.copy(licenseText, writer, encoding);
        IOUtils.copy(licenseText, writer);
        String theString = writer.toString();
        System.out.print(theString);
    } catch (IOException e) {
        throw new Exception(e);
    }
    //return (licenseText);
  }

  protected void saveBytes(String filename, byte[] b)
	  throws Exception
  {
	try {
		FileOutputStream output = new FileOutputStream(new File(filename));
		IOUtils.write(b, output);
	} catch (FileNotFoundException e) {
		throw new Exception(e);
	} catch (IOException e) {
		throw new Exception(e);
	}
  }

  protected int getLicenseVersion()
  {
    return 2;
  }

  private Reader unzipText(byte[] licenseText)
    throws Exception
  {
    ByteArrayInputStream in = new ByteArrayInputStream(licenseText);
    in.skip(LICENSE_PREFIX.length);
    InflaterInputStream zipIn = new InflaterInputStream(in, new Inflater());
    try
    {
      return new InputStreamReader(zipIn, "UTF-8");
    }
    catch (UnsupportedEncodingException e)
    {
      throw new Exception(e);
    }
  }

  private String getLicenseContent(String licenseString)
    throws Exception
  {
    String lengthStr = licenseString.substring(licenseString.lastIndexOf('X') + 3);
    try
    {
      int encodedLicenseLength = Integer.valueOf(lengthStr, 31).intValue();
      return licenseString.substring(0, encodedLicenseLength);
    }
    catch (NumberFormatException e)
    {
      throw new Exception("Could NOT decode license length <" + lengthStr + ">", e);
    }
  }

  private byte[] checkAndGetLicenseText(String licenseContent)
    throws Exception
  {
    byte[] licenseText;
    try
    {
      byte[] decodedBytes = Base64.decodeBase64(licenseContent.getBytes());
      ByteArrayInputStream in = new ByteArrayInputStream(decodedBytes);
      DataInputStream dIn = new DataInputStream(in);
      int textLength = dIn.readInt();
      licenseText = new byte[textLength];
      dIn.read(licenseText);
      byte[] hash = new byte[dIn.available()];
      dIn.read(hash);
      try
      {
        Signature signature = Signature.getInstance("SHA1withDSA");
        signature.initVerify(PUBLIC_KEY);
        signature.update(licenseText);
        if (!signature.verify(hash))
        {
          throw new Exception("Failed to verify the license.");
        }

      }
      catch (InvalidKeyException e)
      {
        throw new Exception(e);
      }
      catch (SignatureException e)
      {
        throw new Exception(e);
      }
      catch (NoSuchAlgorithmException e)
      {
        throw new Exception(e);
      }

    }
    catch (IOException e)
    {
      throw new Exception(e);
    }

    return licenseText;
  }

  private static String removeWhiteSpaces(String licenseData)
  {
    if ((licenseData == null) || (licenseData.length() == 0))
    {
      return licenseData;
    }

    char[] chars = licenseData.toCharArray();
    StringBuffer buf = new StringBuffer(chars.length);
    for (int i = 0; i < chars.length; i++)
    {
      if (!Character.isWhitespace(chars[i]))
      {
        buf.append(chars[i]);
      }
    }

    return buf.toString();
  }

  public static String packLicense(byte[] text, byte[] hash)
    throws Exception
  {
    try
    {
      ByteArrayOutputStream out = new ByteArrayOutputStream();
      DataOutputStream dOut = new DataOutputStream(out);
      dOut.writeInt(text.length);
      dOut.write(text);
      dOut.write(hash);

      byte[] allData = out.toByteArray();
      String result = new String(Base64.encodeBase64(allData)).trim();

      result = result + 'X' + "0" + 2 + Integer.toString(result.length(), 31);
      return split(result);
    }
    catch (IOException e)
    {
      throw new Exception(e);
    }
  }

  private static String split(String licenseData)
  {
    if ((licenseData == null) || (licenseData.length() == 0))
    {
      return licenseData;
    }

    char[] chars = licenseData.toCharArray();
    StringBuffer buf = new StringBuffer(chars.length + chars.length / 76);
    for (int i = 0; i < chars.length; i++)
    {
      buf.append(chars[i]);
      if ((i > 0) && (i % 76 == 0))
      {
        buf.append('\n');
      }
    }

    return buf.toString();
  }

  static public void main(String args[]) 
    throws Exception
  {
//    String lic = "AAABCQ0ODAoPeNptkMtOwzAQRff+CkusjfKkSiQvQuJFII+SBJAqNiYMYNSaaOxE9O9pmko81MVIo\n7l3zlzNRSstTQak3hV1/TgIY9eladZRz3EDkoHpUQ1WfWp+kzfJU0zFJLejnCckRTg2mbTAZz9zA\nuatyIdCeVmoHrQB8aKO26LqRLNu8laQHwK3OMIfe7cfoJI74GldlqJJ86RYdNlbNcGysF28D4Bmh\nniklEpb0FL3IL4GhftficI5UY1vUitzOgrGLtBq3D0D1q/35oDizCUt4ASYZ/z6rm7ZY+X77DZyN\niwMNx5pRcUPxQo/isJV4JBT5oO9yLNzyvkw6xH7d2ng/9u+AZGtfSQwLAIUNXS0YiRanYLneuuRvF/KRpqCKcgCFAtIblcEqI0dugz16/vHA3Q8G5d2X02dh";
	String lic = "AAABEQ0ODAoPeAF1kE1LxDAQhu/5FYGcI/10aSGHtc2h2o+1rQqLl1hHjezGkqTF/fe2teAKehgImTzvPBnSCIu3vcbeJXb9OAhj18VJ2mLPcQNEUjCdlr2VH4pdZ/X2McZ8FIdBzDeIJBqWUyossJmgTkC9DSLvUouLXHagDPBnufC8bHm9q7OGI/ITwqwe4DfQnnooxRFYUhUFr5Nsm68PRGflCCty+I6/B21mPQ+RQkhlQQnVAf/spT6deYWLV6VfhZJmkWYWjF2Dy+H4BLp6uTNTGqMuIg3oEXSWsqvbqqEPpe/Tm8jZ0zDcT5MaXrKpaO5HUbgJHETWz05AnqV/tv5R2g26exMGzlyXHX4B/Fd/MTAsAhQ0b5wdKuuWieiuR4py38TJ6i5WjAIUMSTWS7FKsEGOpTwlX4VmkSp5T7Y=X02dt";
    Decoder d = new Decoder();
    d.doDecode(lic);   
  }
  static
  {
    try
    {
	String pubKeyEncoded = "MIIBtjCCASsGByqGSM44BAEwggEeAoGBANKh8wQdkx7LYai+xWpRrMZh+WOFiBfpYM9Qtpk3FiQgYXcoKrthnqscJDqDxplfn8WCZ5PPiywYLm6syjOc01ksZ5ks7p8EtIYtS7WgcyakR13W3d5FOrJOSmJZi/ir8myZv8e8/Ca1hSMBhgwp/ieCn/CUYAOHnKojIg7u/QWVAhUAjlgGxlPM9aSF/oLmWlf3SLCC9BMCgYA+2YENRJ0uKL0hCcWvoFqEjj9Uyns5Z/Nxm71TGfO5jUm5dKGC0MPzq+0E3kTOVOmOZ46YoXwrQIcaEvkbiiqHfCeA/FIXwwQha7Q+92jEqa8qetA0Fz/I4LiZwvkjppmbI/OS3FC3F+W8TYKcXJ28Hadv48JTkAyag0iE6iz7LgOBhAACgYB+ClOtZQYP75QFu/8r+VXJ0I53lBdb+aihhRfQ0Oy4hbe9MklnAzgX09NbN18MjYlBoghmx5oxXTjlYQWuedEoOFWF1xUHQqX8YC9geeR5bdU2ILX6zVgQMhGQvSTWswopKWjrcic1KooA86z6a+k2hPNFc9EYIunbsY61PH4pLw==";
      KeyFactory keyFactory = KeyFactory.getInstance("DSA");
      PUBLIC_KEY = keyFactory.generatePublic(new X509EncodedKeySpec(Base64.decodeBase64(pubKeyEncoded.getBytes())));
    }
    catch (NoSuchAlgorithmException e)
    {
      throw new Error(e);
    }
    catch (InvalidKeySpecException e)
    {
      throw new Error(e);
    }
  }
}
