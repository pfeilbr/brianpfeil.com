+++
author = "Brian Pfeil"
categories = ["Rust", "playground"]
date = 2018-12-21
description = ""
summary = " "
draft = false
slug = "rust"
tags = ["rust"]
title = "Rust"
repoFullName = "pfeilbr/rust-playground"
repoHTMLURL = "https://github.com/pfeilbr/rust-playground"
truncated = true

+++

<div class="alert alert-info small bg-info" role="alert">
<span class="text-muted">code for article</span>&nbsp;<a href="https://github.com/pfeilbr/rust-playground" target="_blank"><i class="fab fa-github fa-sm"></i>&nbsp;pfeilbr/rust-playground</a>
</div>



learn [Rust](https://www.rust-lang.org/) programming language


## Prerequisites


* [nodemon](https://nodemon.io/) - enables compile and run on file change.


## Development

```sh
# run on file(s) change (ensure `nodemon` is installed)
# turn off dead_code warning
nodemon --exec "RUSTFLAGS=\"$RUSTFLAGS -A dead_code\" cargo run" src/main.rs

# watch tests (run `cargo test` when any file changes)
cargo watch -x check -x test

# show output (e.g. `println!`)
cargo watch -x 'test -- --nocapture'

# to get a stack backtrace on panic
RUST_BACKTRACE=1 cargo run

```

---

## Notes

* compiles to LLVM IR
* guarantees memory safety
* no GC.  compiler generates code at compile time to clean up of memory for variable that go out of scope, etc.  no overhead at runtime for this.  this is what makes it performant. *zero-cost abstractions*
* excellent compiler messages
  * *if you managed to appease the compiler, there’s a good chance your code will work–barring any logic flaws*
* out-of-bounds access at runtime causes the program to immediately stop
* ownership rules apply across multiple threads
* either one mutable reference (read/write) OR many immutable (read-only) references
* no `Null`, only `Option`
* traits are like interfaces in other languages
* includes macros for metaprogramming
  * [dtolnay/cargo-expand: Subcommand to show result of macro expansion](https://github.com/dtolnay/cargo-expand)
* concurrency support via threads, channels, mutex
* can call C code via `extern`
* *Lifetimes are, in some ways, Rust’s most distinctive feature*
  * rust lifetimes are not in other languages. essentially tells the compiler when it can generate code to free memory/variables.  the responsibility the runtime GC in other languages is shifted to you to take care of and think of (*zero cost abstraction? not so much ... there is the human cost*).  see [Understanding lifetimes in Rust - LogRocket Blog](https://blog.logrocket.com/understanding-lifetimes-in-rust/) for details.
* cargo workspaces

---

## `Option` and `Result`

see [Option and Result | Learning Rust](https://learning-rust.github.io/docs/e3.option_and_result.html)

### `Option`

```rust
// An output can have either Some value or no value/ None.
enum Option<T> { // T is a generic and it can contain any type of value.
    Some(T),
    None,
}
```

### `Result`

* If a function can produce an error, we have to use a Result
* used for all I/O, conversions, etc. anything that can fail.

```rust
// A result can represent either success/ Ok or failure/ Err.
enum Result<T, E> { // T and E are generics. T can contain any type of value, E can be any error.
    Ok(T),
    Err(E),
}
```

---

## Smart Pointers (Box, Rc, Arc, Cell)

- Box<T> is for single ownership (single thread, stored on heap).
- Rc<T> is for multiple ownership (single thread, stored on heap).
- Arc<T> is for multiple ownership, but threadsafe (multi-thread, stored on heap).
- Cell<T> is for "interior mutability" for Copy types; that is, when you need to mutate something behind a &T.

---

## Resources

* [The Rust Programming Language book](https://doc.rust-lang.org/stable/book/)
* [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
* [Table of Contents - Rust Cookbook](https://rust-lang-nursery.github.io/rust-cookbook/intro.html)
* [rust-analyzer](https://rust-analyzer.github.io/) - *Bringing a great IDE experience to the Rust programming language.*
* [GitHub - watchexec/cargo-watch: Watches over your Cargo project&#39;s source.](https://github.com/watchexec/cargo-watch)
* [Rust: A Language for the Next 40 Years - Carol Nichols](https://www.youtube.com/watch?v=A3AdN7U24iU)
* [A collection of notable Rust blog posts](https://gist.github.com/brson/a324c83a6af6a8a78dfaa9d33eb9b48e)
* [Understanding lifetimes in Rust - LogRocket Blog](https://blog.logrocket.com/understanding-lifetimes-in-rust/)
* [The Little Book of Rust Macros](http://danielkeep.github.io/tlborm/book/)
* [Yoututbe | Jon Gjengset](https://www.youtube.com/channel/UC_iD0xppBwwsrM9DegC5cQQ) - rust videos
* [dtolnay/cargo-expand: Subcommand to show result of macro expansion](https://github.com/dtolnay/cargo-expand)
* [Wrapper Types in Rust: Choosing Your Guarantees](https://manishearth.github.io/blog/2015/05/27/wrapper-types-in-rust-choosing-your-guarantees/)


