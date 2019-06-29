public class Cipher {

    private static int M = 256;

    public static String hexify(byte[] bytes) {
        StringBuffer b = new StringBuffer();
        for (byte b2 : bytes) {
            String c = Integer.toHexString(b2 & 255);
            if (c.length() == 1) {
                StringBuilder sb = new StringBuilder();
                sb.append('0');
                sb.append(c);
                c = sb.toString();
            }
            b.append(c.toUpperCase());
        }
        return b.toString();
    }

    public static String enc(String plaintext, String key) {
        int i = M;
        int[] a = new int[i];
        byte[] b = new byte[i];
        for (int i2 = 0; i2 < M; i2++) {
            a[i2] = i2;
            b[i2] = (byte) key.charAt(i2 % key.length());
        }
        int i3 = 0;
        int j = 0;
        while (true) {
            int i4 = M;
            if (i3 >= i4 - 1) {
                break;
            }
            j = ((a[i3] + j) + b[i3]) % i4;
            int temp = a[i3];
            a[i3] = a[j];
            a[j] = temp;
            i3++;
        }
        char[] c = plaintext.toCharArray();
        char[] d = new char[plaintext.length()];
        int i5 = 0;
        int j2 = 0;
        for (int k = 0; k < c.length; k++) {
            int i6 = i5 + 1;
            int i7 = M;
            i5 = i6 % i7;
            j2 = (a[i5] + j2) % i7;
            int temp2 = a[i5];
            a[i5] = a[j2];
            a[j2] = temp2;
            d[k] = (char) ((c[k] - i5) ^ ((char) a[(a[i5] + (a[i5] % i7)) % i7]));
        }
        return hexify(new String(d).getBytes());
    }


    public static void main(String[] args){
        String cipher = "C28BC39DC3A6C283C2B3C39DC293C289C2B8C3BAC29EC3A0C3A7C29A1654C3AF28C3A1C2B1215B53";
        String plain = "";
        for(int i = 0; i < 40; i++) {
            for(char c = 0; c < 256; c++){
                String s = enc(plain+c, "E7E64BF658BAB14A25C9D67A054CEBE5");
                if(cipher.startsWith(s)){
                    plain += c;
                    System.out.println(plain);
                    break;
                }
                if(cipher.equals(s))
                    return;
            }
        }
    }

}
