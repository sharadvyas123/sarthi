import { useState, useRef, useEffect } from "react";

const API_URL = "http://localhost:5000/api/message";

const OmSymbol = ({ size = 18, color = "#f59e0b" }) => (
  <svg width={size} height={size} viewBox="0 0 100 100">
    <text
      x="50"
      y="72"
      textAnchor="middle"
      fontSize="72"
      fill={color}
      fontFamily="serif"
    >
      ॐ
    </text>
  </svg>
);

const TypingDots = () => (
  <div
    style={{
      display: "flex",
      gap: "6px",
      alignItems: "center",
      padding: "4px 0",
    }}
  >
    {[0, 1, 2].map((i) => (
      <span
        key={i}
        style={{
          width: "8px",
          height: "8px",
          borderRadius: "50%",
          background: "linear-gradient(135deg, #f97316, #f59e0b)",
          animation: "bounce 1.2s infinite ease-in-out",
          animationDelay: `${i * 0.2}s`,
          display: "block",
        }}
      />
    ))}
  </div>
);

const MessageBubble = ({ msg }) => {
  const isUser = msg.role === "user";
  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        alignItems: "flex-end",
        gap: "10px",
        marginBottom: "22px",
        animation: "fadeSlideUp 0.35s ease forwards",
      }}
    >
      {!isUser && (
        <div
          style={{
            width: "36px",
            height: "36px",
            borderRadius: "50%",
            background: "linear-gradient(135deg, #1a3a5c, #0e6b8a)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
            border: "2px solid #f59e0b",
            boxShadow: "0 0 14px #f59e0b55, 0 0 30px #0e6b8a44",
            fontSize: "16px",
          }}
        >
          🪷
        </div>
      )}
      <div
        style={{
          maxWidth: "70%",
          background: isUser
            ? "linear-gradient(135deg, #c2410c, #ea580c)"
            : "rgba(255,255,255,0.04)",
          border: isUser
            ? "1px solid rgba(251,146,60,0.4)"
            : "1px solid rgba(245,158,11,0.2)",
          color: isUser ? "#fff7ed" : "#fef3c7",
          padding: "13px 18px",
          borderRadius: isUser ? "20px 20px 4px 20px" : "20px 20px 20px 4px",
          fontSize: "14.5px",
          lineHeight: "1.75",
          boxShadow: isUser
            ? "0 4px 24px rgba(234,88,12,0.35)"
            : "0 2px 12px rgba(0,0,0,0.4)",
          whiteSpace: "pre-wrap",
          wordBreak: "break-word",
          backdropFilter: "blur(10px)",
          fontFamily: "'Lora', serif",
          letterSpacing: "0.01em",
        }}
      >
        {msg.content}
      </div>
      {isUser && (
        <div
          style={{
            width: "36px",
            height: "36px",
            borderRadius: "50%",
            background: "linear-gradient(135deg, #431407, #7c2d12)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            flexShrink: 0,
            border: "2px solid rgba(251,146,60,0.5)",
            fontSize: "14px",
            color: "#fb923c",
            fontWeight: "700",
            fontFamily: "'Cinzel', serif",
          }}
        >
          अ
        </div>
      )}
    </div>
  );
};

const SuggestedPrompts = ({ onSelect }) => {
  const prompts = [
    "What does the Gita say about fear?",
    "Explain the concept of Karma Yoga",
    "How to find inner peace according to Krishna?",
    "What is the meaning of Dharma?",
  ];
  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: "10px",
        justifyContent: "center",
        marginTop: "28px",
      }}
    >
      {prompts.map((p) => (
        <button
          key={p}
          onClick={() => onSelect(p)}
          style={{
            background: "rgba(245,158,11,0.08)",
            border: "1px solid rgba(245,158,11,0.3)",
            color: "#fcd34d",
            padding: "9px 16px",
            borderRadius: "20px",
            fontSize: "13px",
            cursor: "pointer",
            transition: "all 0.25s",
            fontFamily: "'Lora', serif",
            letterSpacing: "0.02em",
          }}
          onMouseEnter={(e) => {
            e.target.style.background = "rgba(245,158,11,0.18)";
            e.target.style.borderColor = "#f59e0b";
            e.target.style.boxShadow = "0 0 14px rgba(245,158,11,0.2)";
          }}
          onMouseLeave={(e) => {
            e.target.style.background = "rgba(245,158,11,0.08)";
            e.target.style.borderColor = "rgba(245,158,11,0.3)";
            e.target.style.boxShadow = "none";
          }}
        >
          {p}
        </button>
      ))}
    </div>
  );
};

const MandalaBorder = () => (
  <div
    style={{
      height: "3px",
      background:
        "linear-gradient(90deg, transparent, #f59e0b, #f97316, #0e9eb5, #f59e0b, transparent)",
      opacity: 0.8,
    }}
  />
);

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async (text) => {
    const content = (text || input).trim();
    if (!content || loading) return;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content }]);
    setLoading(true);
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: content }),
      });
      const data = await res.json();
      const reply =
        data.reply ||
        data.message ||
        data.response ||
        data.answer ||
        "Could not reach divine wisdom. Please try again.";
      setMessages((prev) => [...prev, { role: "assistant", content: reply }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "⚠️ Could not reach the server. Please ensure the backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a0f; font-family: 'Lora', serif; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #7c2d12; border-radius: 4px; }
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
          40% { transform: translateY(-7px); opacity: 1; }
        }
        @keyframes fadeSlideUp {
          from { opacity: 0; transform: translateY(12px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes divinePulse {
          0%, 100% { filter: drop-shadow(0 0 4px rgba(245,158,11,0.5)); }
          50% { filter: drop-shadow(0 0 12px rgba(245,158,11,0.9)); }
        }
        @keyframes goldShimmer {
          0% { background-position: -200% center; }
          100% { background-position: 200% center; }
        }
        @keyframes floatOm {
          0%, 100% { transform: translateY(0px) rotate(-2deg); opacity: 0.07; }
          50% { transform: translateY(-14px) rotate(2deg); opacity: 0.12; }
        }
        textarea:focus { outline: none; }
        textarea { resize: none; }
      `}</style>

      {/* Background */}
      <div
        style={{
          position: "fixed",
          inset: 0,
          zIndex: 0,
          background:
            "radial-gradient(ellipse at 20% 20%, #0f1f3d 0%, #0a0a0f 50%, #1a0a00 100%)",
        }}
      >
        <div
          style={{
            position: "absolute",
            right: "6%",
            top: "10%",
            fontSize: "240px",
            color: "#f59e0b",
            fontFamily: "serif",
            animation: "floatOm 9s ease-in-out infinite",
            userSelect: "none",
            pointerEvents: "none",
            lineHeight: 1,
          }}
        >
          ॐ
        </div>
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundImage:
              "radial-gradient(circle, rgba(245,158,11,0.035) 1px, transparent 1px)",
            backgroundSize: "42px 42px",
            pointerEvents: "none",
          }}
        />
      </div>

      <div
        style={{
          display: "flex",
          height: "100vh",
          position: "relative",
          zIndex: 1,
          overflow: "hidden",
        }}
      >
        {/* SIDEBAR */}
        <div
          style={{
            width: sidebarOpen ? "270px" : "0px",
            minWidth: sidebarOpen ? "270px" : "0px",
            transition: "all 0.35s cubic-bezier(0.4,0,0.2,1)",
            overflow: "hidden",
            background: "rgba(8,5,2,0.94)",
            borderRight: "1px solid rgba(245,158,11,0.15)",
            display: "flex",
            flexDirection: "column",
            backdropFilter: "blur(20px)",
          }}
        >
          <MandalaBorder />
          <div style={{ padding: "24px 20px 16px", whiteSpace: "nowrap" }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
                marginBottom: "30px",
              }}
            >
              <div
                style={{
                  width: "42px",
                  height: "42px",
                  borderRadius: "50%",
                  background: "linear-gradient(135deg, #1a3a5c, #0e6b8a)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  border: "2px solid #f59e0b",
                  boxShadow: "0 0 20px #f59e0b50",
                  fontSize: "20px",
                }}
              >
                🪷
              </div>
              <div>
                <span
                  style={{
                    fontSize: "22px",
                    fontWeight: "700",
                    letterSpacing: "4px",
                    fontFamily: "'Cinzel', serif",
                    background:
                      "linear-gradient(90deg, #fbbf24, #f97316, #fbbf24)",
                    backgroundSize: "200% auto",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                    animation: "goldShimmer 4s linear infinite",
                    display: "block",
                  }}
                >
                  SARTHI
                </span>
                <div
                  style={{
                    fontSize: "10px",
                    color: "#78350f",
                    letterSpacing: "2.5px",
                    fontFamily: "'Cinzel', serif",
                    marginTop: "2px",
                  }}
                >
                  DIVINE WISDOM
                </div>
              </div>
            </div>

            <button
              onClick={() => setMessages([])}
              style={{
                width: "100%",
                padding: "11px 14px",
                background: "rgba(245,158,11,0.08)",
                border: "1px solid rgba(245,158,11,0.25)",
                borderRadius: "10px",
                color: "#fcd34d",
                fontSize: "13px",
                fontWeight: "500",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                gap: "10px",
                fontFamily: "'Lora', serif",
                transition: "all 0.2s",
                letterSpacing: "0.03em",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "rgba(245,158,11,0.16)";
                e.currentTarget.style.boxShadow =
                  "0 0 16px rgba(245,158,11,0.15)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "rgba(245,158,11,0.08)";
                e.currentTarget.style.boxShadow = "none";
              }}
            >
              <OmSymbol size={16} color="#f59e0b" /> New Conversation
            </button>
          </div>

          <div
            style={{
              margin: "0 20px 16px",
              height: "1px",
              background:
                "linear-gradient(90deg, transparent, rgba(245,158,11,0.25), transparent)",
            }}
          />

          <div style={{ flex: 1, padding: "0 20px", overflow: "auto" }}>
            <p
              style={{
                fontSize: "10px",
                color: "#78350f",
                textTransform: "uppercase",
                letterSpacing: "2px",
                marginBottom: "12px",
                fontFamily: "'Cinzel', serif",
              }}
            >
              Recent
            </p>
            {messages.length === 0 ? (
              <p
                style={{
                  fontSize: "13px",
                  color: "#3d1a00",
                  fontStyle: "italic",
                }}
              >
                No conversations yet
              </p>
            ) : (
              <div
                style={{
                  padding: "10px 13px",
                  borderRadius: "8px",
                  background: "rgba(245,158,11,0.07)",
                  border: "1px solid rgba(245,158,11,0.15)",
                  fontSize: "13px",
                  color: "#fbbf24",
                  cursor: "pointer",
                  fontFamily: "'Lora', serif",
                }}
              >
                {messages[0]?.content?.slice(0, 32)}...
              </div>
            )}
          </div>

          <div
            style={{
              margin: "0 20px 8px",
              height: "1px",
              background:
                "linear-gradient(90deg, transparent, rgba(245,158,11,0.2), transparent)",
            }}
          />
          <div style={{ padding: "14px 20px 20px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div
                style={{
                  width: "34px",
                  height: "34px",
                  borderRadius: "50%",
                  background: "linear-gradient(135deg, #431407, #7c2d12)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "14px",
                  color: "#fb923c",
                  fontWeight: "700",
                  border: "1px solid rgba(251,146,60,0.4)",
                  fontFamily: "'Cinzel', serif",
                }}
              >
                अ
              </div>
              <div>
                <p
                  style={{
                    fontSize: "13px",
                    fontWeight: "500",
                    color: "#fde68a",
                    fontFamily: "'Cinzel', serif",
                  }}
                >
                  Seeker
                </p>
                <p style={{ fontSize: "11px", color: "#78350f" }}>
                  On the path of Gyan
                </p>
              </div>
            </div>
          </div>
          <MandalaBorder />
        </div>

        {/* MAIN AREA */}
        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
          }}
        >
          {/* TOP BAR */}
          <div
            style={{
              height: "58px",
              display: "flex",
              alignItems: "center",
              padding: "0 22px",
              gap: "14px",
              background: "rgba(8,5,2,0.88)",
              backdropFilter: "blur(16px)",
              borderBottom: "1px solid rgba(245,158,11,0.12)",
            }}
          >
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              style={{
                background: "none",
                border: "none",
                color: "#a16207",
                cursor: "pointer",
                fontSize: "20px",
                padding: "4px",
                display: "flex",
                alignItems: "center",
                transition: "color 0.2s",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = "#f59e0b")}
              onMouseLeave={(e) => (e.currentTarget.style.color = "#a16207")}
            >
              ☰
            </button>

            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div style={{ animation: "divinePulse 3s infinite" }}>
                <OmSymbol size={22} color="#f59e0b" />
              </div>
              <span
                style={{
                  fontSize: "15px",
                  fontFamily: "'Cinzel', serif",
                  background: "linear-gradient(90deg, #fbbf24, #f97316)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  fontWeight: "600",
                  letterSpacing: "2px",
                }}
              >
                SARTHI
              </span>
              <span
                style={{
                  fontSize: "12px",
                  color: "#92400e",
                  fontFamily: "'Lora', serif",
                  fontStyle: "italic",
                }}
              >
                — Bhagavad Gita AI
              </span>
            </div>

            <div
              style={{
                marginLeft: "auto",
                display: "flex",
                alignItems: "center",
                gap: "6px",
              }}
            >
              <div
                style={{
                  width: "7px",
                  height: "7px",
                  borderRadius: "50%",
                  background: "#4ade80",
                  boxShadow: "0 0 8px #4ade80",
                }}
              />
              <span
                style={{
                  fontSize: "11px",
                  color: "#78350f",
                  fontFamily: "'Cinzel', serif",
                  letterSpacing: "1px",
                }}
              >
                ONLINE
              </span>
            </div>
          </div>

          {/* MESSAGES */}
          <div style={{ flex: 1, overflowY: "auto", padding: "32px 22px" }}>
            <div style={{ maxWidth: "780px", margin: "0 auto" }}>
              {messages.length === 0 && (
                <div
                  style={{
                    textAlign: "center",
                    paddingTop: "50px",
                    animation: "fadeSlideUp 0.6s ease",
                  }}
                >
                  <div
                    style={{
                      fontSize: "64px",
                      marginBottom: "8px",
                      filter: "drop-shadow(0 0 24px #f59e0b)",
                    }}
                  >
                    🦚
                  </div>
                  <div
                    style={{
                      fontSize: "12px",
                      color: "#78350f",
                      letterSpacing: "4px",
                      fontFamily: "'Cinzel', serif",
                      marginBottom: "14px",
                    }}
                  >
                    ॐ नमो भगवते वासुदेवाय
                  </div>
                  <h1
                    style={{
                      fontSize: "36px",
                      fontWeight: "700",
                      fontFamily: "'Cinzel', serif",
                      background:
                        "linear-gradient(135deg, #fde68a 20%, #f97316 60%, #fbbf24)",
                      WebkitBackgroundClip: "text",
                      WebkitTextFillColor: "transparent",
                      marginBottom: "12px",
                    }}
                  >
                    Namaste, Seeker
                  </h1>

                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "12px",
                      justifyContent: "center",
                      margin: "16px 0",
                    }}
                  >
                    <div
                      style={{
                        flex: 1,
                        maxWidth: "80px",
                        height: "1px",
                        background:
                          "linear-gradient(90deg, transparent, #f59e0b)",
                      }}
                    />
                    <OmSymbol size={22} color="#f59e0b" />
                    <div
                      style={{
                        flex: 1,
                        maxWidth: "80px",
                        height: "1px",
                        background:
                          "linear-gradient(90deg, #f59e0b, transparent)",
                      }}
                    />
                  </div>

                  <p
                    style={{
                      fontSize: "15px",
                      color: "#d97706",
                      lineHeight: "1.8",
                      maxWidth: "460px",
                      margin: "0 auto",
                      fontFamily: "'Lora', serif",
                      fontStyle: "italic",
                    }}
                  >
                    Seek wisdom from the Bhagavad Gita — ask your questions and
                    receive guidance through its sacred shlokas and timeless
                    teachings.
                  </p>
                  <SuggestedPrompts onSelect={sendMessage} />
                </div>
              )}

              {messages.map((msg, i) => (
                <MessageBubble key={i} msg={msg} />
              ))}

              {loading && (
                <div
                  style={{
                    display: "flex",
                    alignItems: "flex-end",
                    gap: "10px",
                    marginBottom: "20px",
                    animation: "fadeSlideUp 0.3s ease",
                  }}
                >
                  <div
                    style={{
                      width: "36px",
                      height: "36px",
                      borderRadius: "50%",
                      background: "linear-gradient(135deg, #1a3a5c, #0e6b8a)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      border: "2px solid #f59e0b",
                      boxShadow: "0 0 14px #f59e0b55",
                      fontSize: "16px",
                      flexShrink: 0,
                    }}
                  >
                    🪷
                  </div>
                  <div
                    style={{
                      background: "rgba(255,255,255,0.04)",
                      border: "1px solid rgba(245,158,11,0.2)",
                      padding: "13px 18px",
                      borderRadius: "20px 20px 20px 4px",
                      backdropFilter: "blur(8px)",
                    }}
                  >
                    <TypingDots />
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
          </div>

          {/* INPUT BAR */}
          <div
            style={{
              padding: "0 22px 22px",
              background: "rgba(8,5,2,0.92)",
              backdropFilter: "blur(16px)",
              borderTop: "1px solid rgba(245,158,11,0.12)",
            }}
          >
            <MandalaBorder />
            <div style={{ maxWidth: "780px", margin: "12px auto 0" }}>
              <div
                style={{
                  display: "flex",
                  alignItems: "flex-end",
                  gap: "10px",
                  background: "rgba(255,255,255,0.03)",
                  border: `1px solid ${input ? "rgba(245,158,11,0.55)" : "rgba(245,158,11,0.15)"}`,
                  borderRadius: "16px",
                  padding: "13px 15px",
                  transition: "all 0.25s",
                  boxShadow: input
                    ? "0 0 28px rgba(245,158,11,0.1), inset 0 0 20px rgba(245,158,11,0.03)"
                    : "none",
                }}
              >
                <div style={{ paddingBottom: "4px", opacity: 0.5 }}>
                  <OmSymbol size={18} color="#f59e0b" />
                </div>
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKey}
                  placeholder="Ask your question to Krishna's wisdom..."
                  rows={1}
                  style={{
                    flex: 1,
                    background: "transparent",
                    border: "none",
                    color: "#fde68a",
                    fontSize: "14.5px",
                    fontFamily: "'Lora', serif",
                    lineHeight: "1.7",
                    maxHeight: "140px",
                    overflowY: "auto",
                    caretColor: "#f59e0b",
                  }}
                  onInput={(e) => {
                    e.target.style.height = "auto";
                    e.target.style.height =
                      Math.min(e.target.scrollHeight, 140) + "px";
                  }}
                />
                <button
                  onClick={() => sendMessage()}
                  disabled={!input.trim() || loading}
                  style={{
                    width: "38px",
                    height: "38px",
                    borderRadius: "10px",
                    background:
                      input.trim() && !loading
                        ? "linear-gradient(135deg, #b45309, #f59e0b)"
                        : "rgba(255,255,255,0.04)",
                    border:
                      input.trim() && !loading
                        ? "1px solid rgba(251,191,36,0.4)"
                        : "1px solid rgba(255,255,255,0.06)",
                    cursor: input.trim() && !loading ? "pointer" : "default",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    transition: "all 0.25s",
                    flexShrink: 0,
                    boxShadow:
                      input.trim() && !loading
                        ? "0 0 18px rgba(245,158,11,0.4)"
                        : "none",
                  }}
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path
                      d="M22 2L11 13"
                      stroke={input.trim() && !loading ? "#fff7ed" : "#44260a"}
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <path
                      d="M22 2L15 22L11 13L2 9L22 2Z"
                      stroke={input.trim() && !loading ? "#fff7ed" : "#44260a"}
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </button>
              </div>
              <p
                style={{
                  textAlign: "center",
                  fontSize: "11px",
                  color: "#3d1a00",
                  marginTop: "10px",
                  fontFamily: "'Cinzel', serif",
                  letterSpacing: "0.5px",
                }}
              >
                Press{" "}
                <kbd
                  style={{
                    background: "rgba(245,158,11,0.08)",
                    padding: "1px 6px",
                    borderRadius: "4px",
                    color: "#78350f",
                    border: "1px solid rgba(245,158,11,0.15)",
                  }}
                >
                  Enter
                </kbd>{" "}
                to seek ·{" "}
                <kbd
                  style={{
                    background: "rgba(245,158,11,0.08)",
                    padding: "1px 6px",
                    borderRadius: "4px",
                    color: "#78350f",
                    border: "1px solid rgba(245,158,11,0.15)",
                  }}
                >
                  Shift+Enter
                </kbd>{" "}
                for new line
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
