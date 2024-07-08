## linearizability checker

Proof-of-concept how a linearizability checker could work based on the captured HTTP request/response. Most research out there state and give the example that linearizability works well with distributed file systems or something similar, like key-file systems-based (e.g., HDFS), but it hasn't yet been fully explored how to integrate during interoperability exchange between data especially when the systems were using REST/gRPC-based. The provided PoC should be sufficient and implemented in the simplest way possible, but it still needs fine-tuning to operate seamlessly. Let's say you'll have distributed systems that have several services. All you need to do is:

1. Perform basic HTTP requests, such as those corresponding to the PUT and GET methods
2. Logs must be generated and captured. In this context, you need some kind of middleware to integrate between captured logs to be analyzed and determined using this code
3. Change the path where all your logs are stored and run the `checker.py` command
4. In this provided code, you may change with the different logs: `failure_logs` to simulate when the system having a disruption, `success_logs` to simulate when the system don't have an issue (feel free to change the attributes in the provided logs)

**Notes**

1. As you may be aware, every distributed system has a different behavior. You need to adjust the expected response within the logs based on your needs or requirements
2. Some observation: it performs well with the small log history, but it will cause another issue when run over much more logs that contain multiple or different records. You may use a better tools like [Porcupine](https://github.com/anishathalye/porcupine) for faster checking
3. Did this perform well to capture subtle bugs like non-deterministic behavior or interleaving bugs? honestly, i can't say for sure, since it's probably the most intricate thing to encounter to find the exact pattern, but i could say that performing random operations (e.g., ad-hoc testing) can probing any intermediates or delay bugs

**Future considerations**

In practice, the linearizability must be tested to verify the correctness of the concurrency that's happening on the distributed systems. By all means, it's performed to check the consistency (and safety) between every concurrent history or record in the previous sequences, which should remain the same in the next sequences. However, the PoC that was provided only checked for single history (based on the logs); for future work, we could both combine and merge all of the recorded logs and determine based on what could be a possible interleaving issue that was happening by comparing the first logs and second logs.