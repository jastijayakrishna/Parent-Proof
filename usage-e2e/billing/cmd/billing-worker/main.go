package main

import (
	"context"
	"fmt"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	pb "example.com/billing/gen/paymentsv1"
	"example.com/billing/internal/ledger"
)

func main() {
	conn, err := grpc.NewClient("payments:443", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		panic(err)
	}
	l := ledger.New(pb.NewPaymentsClient(conn))
	total, err := l.Total(context.Background(), "ch_1")
	fmt.Println(total, err)
}
