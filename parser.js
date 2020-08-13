var saxStream = require("./sax-js/lib/sax.js").createStream(true);
var fs        = require('fs');

function create_packet() {
	packet = {
		timestamp: "",
		eth: {
			proto: "",
			src: "",
			dst: "",
		},
		vlan: {
			proto: "",
			id: "",
		},
		ip: {
			src: "",
			dst: "",
			version: "",
			len: "",
			proto: "",
			ttl: "",
			flags: ""
		},
		gre: {
			proto: "",
			sequence_number: "",
			ack_sequence: ""
		},
		ppp: {
			proto: "",
			ip: {
				src: "",
				dst: "",
				version: "",
				proto: "",
				len: "",
				ttl: "",
				flags: ""
			}
		},
		tcp : {
			srcport: "",
			dstport: "",
			stream_idx: "",
			flags: "",
			window_size: "",
			window_size_scalefactor: "",
			len: "",
			seq: "",
			ack: ""
		},
		udp : {
			srcport: "",
			dstport: "",
			len: ""
		}
	};
	return packet;
}


saxStream.on("error", function (e) {
  this._parser.error = null;
  this._parser.resume();
});

saxStream.on("closetag", function(tag) {
	if(tag === "packet") {
		console.log(JSON.stringify(packet));
	}
});

var packet = null;

saxStream.on("opentag", function (tag) {
	if (tag.name === "packet") {
		packet = create_packet();
	}  else if (tag.name === "field") {

		if (tag.attributes["name"] === "frame.time_epoch") {
			packet.timestamp = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "eth.type") {
			packet.eth.proto = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "eth.dst") {
			packet.eth.dst = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "eth.src") {
			packet.eth.src = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "eth.len") {
			packet.eth.len = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "vlan.id") {
			packet.vlan.id = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "vlan.etype") {
			packet.vlan.proto = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "vlan.len") {
			packet.vlan.len = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "ip.flags") {
			if (packet.ip.flags === "") {
				packet.ip.flags = tag.attributes["show"];	
			} else {
				if (packet.ppp.proto  === "33") {
					if (packet.ppp.ip.flags === "") {
						packet.ppp.ip.flags = tag.attributes["show"];
					}
				}
			}
		}
		
		if (tag.attributes["name"] === "ip.version") {
			if (packet.ip.version === "") {
				packet.ip.version = tag.attributes["show"];	
			} else {
				if (packet.ppp.proto  === "33") {
					if (packet.ppp.ip.version === "") {
						packet.ppp.ip.version = tag.attributes["show"];
					}
				}
			}
		}

		if (tag.attributes["name"] === "ip.proto") {
			if (packet.ip.proto === "") {
				packet.ip.proto = tag.attributes["show"];	
			} else {
				if (packet.ppp.proto  === "33") {
					if (packet.ppp.ip.proto === "") {
						packet.ppp.ip.proto = tag.attributes["show"];
					}
				}
			}
		}

		if (tag.attributes["name"] === "ip.len") {
			if (packet.ip.len === "") {
				packet.ip.len = tag.attributes["show"];	
			} else {
				if (packet.ppp.proto  === "33") {
					if (packet.ppp.ip.len === "") {
						packet.ppp.ip.len = tag.attributes["show"];
					}
				}
			}
		}

		if (tag.attributes["name"] === "ip.ttl") {
			if (packet.ip.ttl === "") {
				packet.ip.ttl = tag.attributes["show"];	
			} else {
				if (packet.ppp.proto  === "33") {
					if (packet.ppp.ip.ttl === "") {
						packet.ppp.ip.ttl = tag.attributes["show"];
					}
				}
			}
		}

		if (tag.attributes["name"] === "ip.src") {
			if (packet.ip.src === "") {
				packet.ip.src = tag.attributes["show"];	
			} else {
				if (packet.ppp.proto  === "33") {
					if (packet.ppp.ip.src === "") {
						packet.ppp.ip.src = tag.attributes["show"];
					}
				}	
			}
		}

		if (tag.attributes["name"] === "ip.dst") {
			if (packet.ip.dst === "") {
				packet.ip.dst = tag.attributes["show"];	
			} else {
				if (packet.ppp.proto  === "33") {
					if (packet.ppp.ip.dst === "") {
						packet.ppp.ip.dst = tag.attributes["show"];
					}
				}	
			}

		}

		if (tag.attributes["name"] === "gre.proto") {
			packet.gre.proto = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "ppp.protocol") {
			packet.ppp.proto = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "udp.srcport") {
			packet.udp.srcport = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "udp.dstport") {
			packet.udp.dstport = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "udp.length") {
			packet.udp.len = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "tcp.srcport") {
			packet.tcp.srcport = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "tcp.dstport") {
			packet.tcp.dstport = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "tcp.stream") {
			packet.tcp.stream_idx = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "tcp.len") {
			packet.tcp.len = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "tcp.flags") {
			packet.tcp.flags = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "tcp.window_size") {
			packet.tcp.window_size = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "tcp.window_size_scalefactor") {
			packet.tcp.window_size_scalefactor = tag.attributes["show"];
		}

		if (tag.attributes["name"] === "tcp.seq") {
			packet.tcp.seq = tag.attributes["show"];
		}
		
		if (tag.attributes["name"] === "tcp.ack") {
			packet.tcp.ack = tag.attributes["show"];
		}
	}
});


process.stdin.pipe(saxStream);

