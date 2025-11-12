<h1>A chess question</h1>
<p>This repository contains a python program that that answer a question: <strong>which BLACK pieces are capturable</strong> by a single WHITE piece on a given board state.</p>

<h2>Contents</h2>
<ul>
  <li><strong>Source code</strong> — <code>chess_question.py</code></li>
  <li><strong>Example</strong> — transcript of a typical session of the program (see below)</li>
</ul>

<h2>Summary</h2>
<ul>
  <li>Program prompts for one WHITE piece (currently <code>pawn</code> or <code>rook</code>) and 1-16 BLACK pieces.</li>
  <li>Validates input format (<code>&lt;piece&gt; &lt;square&gt;</code>, e.g., <code>rook a1</code>), board bounds (a1–h8), and square occupancy.</li>
  <li>Computes and prints list of black pieces that are capturable by the given WHITE piece according to chess rules implemented.</li>
</ul>

<h2>How to Run</h2>
<ol>
  <li>Install Python 3.10+</li>
  <li>Download chess_question.py and open a terminal in the project root folder</li>
  <li>Run the app with this command:
    <pre><code>python chess_question.py</code></pre>
  </li>
</ol>

<h2>Usage</h2>
<p>Follow the on-screen prompts. The program will:</p>
<ol>
  <li>Ask for a WHITE piece and its square (only <code>pawn</code> or <code>rook</code> are allowed for WHITE piece input in current version.</li>
  <li>Let you add 1–16 BLACK pieces one by one (piece type and square), validating each entry.</li>
  <li>Output which BLACK pieces are currently capturable by the WHITE piece.</li>
</ol>

<h3>Input format</h3>
<ul>
  <li><code>&lt;piece&gt; &lt;square&gt;</code>, e.g., <code>pawn e4</code>, <code>rook a1</code>, <code>bishop c6</code></li>
  <li>Squares must be algebraic notation in <code>a1</code>–<code>h8</code>.</li>
  <li>Each square can hold at most one piece; duplicates are rejected.</li>
</ul>

<h3>Example session</h3>
<pre><code>Enter WHITE piece and position (pawn/rook), e.g., 'pawn e4': rook e6
Added WHITE rook on e6.
Now add BLACK pieces one by one (any valid chess piece).
Format: 'bishop d6'. Add at least 1 and max 16 pieces. Type 'done' when finished

Add BLACK piece (or 'done'): king e8
Added BLACK king on e8.
Add BLACK piece (or 'done'): queen d6
Added BLACK queen on d6.
Add BLACK piece (or 'done'): pawn b6
Added BLACK pawn on b6.
Add BLACK piece (or 'done'): knight e5
Added BLACK knight on e5.
Add BLACK piece (or 'done'): bishop f6
Added BLACK bishop on f6.
Add BLACK piece (or 'done'): done

=== Result ===
The white rook on e6 can capture these squares:
d6 queen
e5 knight
f6 bishop
</code></pre>

<h2>Rules Implemented</h2>
<ul>
  <li><strong>White Rook</strong>: horizontal/vertical capture within the straight line (first encounter breaks the loop).</li>
  <li><strong>White Pawn</strong>: diagonal capture (e.g., from <code>e4</code> it can capture on <code>d5</code> or <code>f5</code>), no forward captures, only first piece encountered can be captured.</li>
  <li><strong>Black Pieces</strong>: may be any chess piece; only their positions matter as occupation.</li>
</ul>
