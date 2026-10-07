package main

import (
	"context"
	"fmt"

	"google.golang.org/protobuf/encoding/protojson"

	pb "example.com/billing/gen/paymentsv1"
)

func refund(ctx context.Context, client pb.PaymentsClient, id string) error {
	charge, err := client.GetCharge(ctx, &pb.GetChargeRequest{Id: id})
	if err != nil {
		return err
	}
	if charge.GetAmountCents() == 0 {
		return nil
	}
	for _, t := range charge.Tags {
		fmt.Println(t)
	}
	return nil
}

func decode(b []byte) (*pb.Charge, error) {
	var c pb.Charge
	if err := protojson.Unmarshal(b, &c); err != nil {
		return nil, err
	}
	return &c, nil
}

func main() {
	fmt.Println(refund(context.Background(), nil, "ch_1"))
}
