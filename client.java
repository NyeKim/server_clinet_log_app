//  FILE : client.java
//  PROJECT : SENG2040 - Assignment #3
//  PROGRAMMER : Eunhye Kim
//  FIRST VERSION : 2020-11-15
//  DESCRIPTION : This is a client tool written by Java.
//  This client tool is for sending a message through TCP/IP socket to test the server.


package tool;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.Scanner;
import java.nio.charset.Charset;

//NAME : client
//PURPOSE : The client class has been created to send a message to the server for the test performance of the server.
//The client class works with arguments from a command line and automatically creates a client socket to connect to the server.
//The client also has the ability to get input messages from a user and convert it to the socket-server-available type. 
public class client {

	public static void main(String[] args) {
		
		//parsing arguments
		int ConnPort = Integer.parseInt(args[0]);
		String ServerIP = args[1];
		
		final Charset UTF8_CHARSET = Charset.forName("UTF-8");
	
		try (Socket client = new Socket()) {
	
			InetSocketAddress clientSock = new InetSocketAddress(ServerIP, ConnPort);
	
			client.connect(clientSock);
	
			try (OutputStream send = client.getOutputStream()) {
		
				try (Scanner sc = new Scanner(System.in)) {
	
					while (true) {
	
						String Msg = sc.nextLine();
						//convert an input to UTF8_CHARSET
						byte[] ConvertedMsg = Msg.getBytes(UTF8_CHARSET);
	
						send.write(ConvertedMsg);
	
					}
				}
			}
		} 
		catch (Throwable e) {
			e.printStackTrace();
		}
	}
}

