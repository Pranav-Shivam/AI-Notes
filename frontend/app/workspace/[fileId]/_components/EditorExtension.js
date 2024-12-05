"use client";
import {
  AlignCenter,
  AlignJustify,
  AlignLeft,
  AlignRight,
  Bold,
  Code,
  Italic,
  List,
  ListOrdered,
  Sparkle,
  Strikethrough,
  Subscript,
  Superscript,
  Underline,
  Mic,
} from "lucide-react";
import React from "react";

const EditorExtensions = ({ editor }) => {
  const onAiClick = () => {
    const selectedText = editor.state.doc.textBetween(
      editor.state.selection.from,
      editor.state.selection.to,
      "  "
    );
    console.log(selectedText);
  };

  const [isListening, setIsListening] = React.useState(false);
  const [error, setError] = React.useState(null);
  const recognition = React.useRef(null);
  const [isBrowserSupported, setIsBrowserSupported] = React.useState(false);

  // Initialize speech recognition
  React.useEffect(() => {
    // Check browser support
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
      recognition.current = new SpeechRecognition();
      recognition.current.lang = "en-US";
      recognition.current.continuous = false; // Changed to false to prevent repetition
      recognition.current.interimResults = false; // Changed to false for final results only
      setIsBrowserSupported(true);

      // Handle results
      recognition.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (editor) {
          editor.commands.insertContent(transcript + " ");
        }
      };

      // Handle errors
      recognition.current.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        setError(`Error: ${event.error}`);
        setIsListening(false);
      };

      // Handle end of speech
      recognition.current.onend = () => {
        setIsListening(false);
      };
    } else {
      setError("Speech recognition not supported in this browser");
      setIsBrowserSupported(false);
    }

    // Cleanup
    return () => {
      if (recognition.current) {
        recognition.current.abort();
      }
    };
  }, [editor]);

  // Handle mic button click
  const toggleMic = async () => {
    try {
      if (isListening) {
        recognition.current.stop();
        setIsListening(false);
      } else {
        // Request microphone permission
        await navigator.mediaDevices.getUserMedia({ audio: true });
        recognition.current.start();
        setIsListening(true);
        setError(null);
      }
    } catch (err) {
      console.error("Microphone error:", err);
      setError("Please allow microphone access");
      setIsListening(false);
    }
  };

  if (!editor) {
    return null;
  }

  return (
    editor && (
      <div className="p-5">
        <div className="control-group">
          <div className="button-group flex gap-3 items-center">
            <button
              onClick={() =>
                editor.chain().focus().toggleHeading({ level: 1 }).run()
              }
              className={`h-6 w-6 flex items-center justify-center ${
                editor.isActive("heading", { level: 1 }) ? "text-blue-600" : ""
              }`}
            >
              <p className="text-2xl leading-none">H1</p>
            </button>
            <button
              onClick={() =>
                editor.chain().focus().toggleHeading({ level: 2 }).run()
              }
              className={`h-6 w-6 flex items-center justify-center ${
                editor.isActive("heading", { level: 2 }) ? "text-blue-600" : ""
              }`}
            >
              <p className="text-2xl leading-none">H2</p>
            </button>
            <button
              onClick={() =>
                editor.chain().focus().toggleHeading({ level: 3 }).run()
              }
              className={`h-6 w-6 flex items-center justify-center ${
                editor.isActive("heading", { level: 3 }) ? "text-blue-600" : ""
              }`}
            >
              <p className="text-2xl leading-none">H3</p>
            </button>
            <button
              onClick={() => editor.chain().focus().toggleBold().run()}
              className={editor.isActive("bold") ? "text-blue-600" : ""}
            >
              <Bold />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleItalic().run()}
              className={editor.isActive("italic") ? "text-blue-500" : ""}
            >
              <Italic />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleUnderline().run()}
              className={editor.isActive("underline") ? "text-blue-600" : ""}
            >
              <Underline />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleSubscript().run()}
              className={editor.isActive("subscript") ? "text-blue-600" : ""}
            >
              <Subscript />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleSuperscript().run()}
              className={editor.isActive("superscript") ? "text-blue-600" : ""}
            >
              <Superscript />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleStrike().run()}
              className={editor.isActive("strike") ? "text-blue-600" : ""}
            >
              <Strikethrough />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleOrderedList().run()}
              className={editor.isActive("orderedList") ? "text-blue-600" : ""}
            >
              <ListOrdered />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleBulletList().run()}
              className={editor.isActive("bulletList") ? "text-blue-600" : ""}
            >
              <List />
            </button>
            <button
              onClick={() => editor.chain().focus().setTextAlign("left").run()}
              className={
                editor.isActive({ textAlign: "left" }) ? "text-blue-600" : ""
              }
            >
              <AlignLeft />
            </button>
            <button
              onClick={() =>
                editor.chain().focus().setTextAlign("center").run()
              }
              className={
                editor.isActive({ textAlign: "center" }) ? "text-blue-600" : ""
              }
            >
              <AlignCenter />
            </button>
            <button
              onClick={() => editor.chain().focus().setTextAlign("right").run()}
              className={
                editor.isActive({ textAlign: "right" }) ? "text-blue-600" : ""
              }
            >
              <AlignRight />
            </button>
            <button
              onClick={() =>
                editor.chain().focus().setTextAlign("justify").run()
              }
              className={
                editor.isActive({ textAlign: "justify" }) ? "text-blue-600" : ""
              }
            >
              <AlignJustify />
            </button>
            <button
              onClick={() => editor.chain().focus().toggleCode().run()}
              className={editor.isActive("code") ? "text-blue-600" : ""}
            >
              <Code />
            </button>
            <button
              onClick={() => onAiClick()}
              className={"hover:text-blue-700"}
            >
              <Sparkle />
            </button>
            {/* Mic button */}
            <button
              onClick={toggleMic}
              disabled={!isBrowserSupported}
              className={`
               rounded-md transition-colors
              ${
                !isBrowserSupported
                  ? "opacity-50 cursor-not-allowed"
                  : "hover:bg-gray-100"
              }
              ${isListening ? "text-red-500" : ""}
            `}
              title={
                !isBrowserSupported
                  ? "Speech recognition not supported in this browser"
                  : isListening
                  ? "Stop recording"
                  : "Start recording"
              }
            >
              <Mic
                className={`w-5 h-5 ${isListening ? "animate-pulse" : ""}`}
              />
            </button>
          </div>
        </div>
      </div>
    )
  );
};

export default EditorExtensions;
