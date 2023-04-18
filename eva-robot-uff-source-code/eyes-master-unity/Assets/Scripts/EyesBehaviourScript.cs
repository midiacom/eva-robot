using UnityEngine;
using System;
using System.Net;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

public class EyesBehaviourScript : MonoBehaviour
{
    private Animator anim { get; set; }
    private bool state { get; set; }
    private string[] names { get; set; }
    private MqttClient client;
    private int option;
    // Start is called before the first frame update
    void Start()
    {
        anim = GetComponent<Animator>();
        names = new[] { "Angry 0", "Bored 0", "Sad 0", "Happy 0", "Surprised 0" };
        state = true;
        option = 0;

        client = new MqttClient("broker.hivemq.com", 1883, false, null);

        // register to message received 
        client.MqttMsgPublishReceived += client_MqttMsgPublishReceived;

        string clientId = Guid.NewGuid().ToString();
        client.Connect(clientId);

        // subscribe to the topic "/home/temperature" with QoS 2 
        client.Subscribe(new string[] { "disi/emotion" }, new byte[] { MqttMsgBase.QOS_LEVEL_AT_MOST_ONCE });
    }

    void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
    {
        option = int.Parse(System.Text.Encoding.UTF8.GetString(e.Message));
        Debug.Log("Received: " + System.Text.Encoding.UTF8.GetString(e.Message));
    }

    // Update is called once per frame
    void Update()
    {       
        var temp = anim.GetCurrentAnimatorStateInfo(0);

        if (!temp.IsName("New State"))
        {
            if (temp.IsName(names[0]) || temp.IsName(names[1]) || temp.IsName(names[2]) || temp.IsName(names[3]) || temp.IsName(names[4]))
            {
                state = true;
            }
            if (!temp.IsName(names[0]) && !temp.IsName(names[1]) && !temp.IsName(names[2]) && !temp.IsName(names[3]) && !temp.IsName(names[4]) && state)
            {
                state = false;
                option = 0;
                anim.SetInteger("Option", option);
            }
        }

        //if (Input.GetKey(KeyCode.A))
        //{
        anim.SetInteger("Option", option);
        //}
        //if (Input.GetKey(KeyCode.B))
        //{
        //    anim.SetInteger("Option", 2);
        //}
        //if (Input.GetKey(KeyCode.S))
        //{
        //    anim.SetInteger("Option", 3);
        //}
        //if (Input.GetKey(KeyCode.H))
        //{
        //    anim.SetInteger("Option", 4);
        //}
        //if (Input.GetKey(KeyCode.U))
        //{
        //    anim.SetInteger("Option", 5);
        //}
    }
}
